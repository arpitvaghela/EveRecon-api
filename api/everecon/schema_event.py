from random import sample

import graphene
from django.contrib.auth.models import User
from django_graphene_permissions import permissions_checker, check_object_permissions, PermissionDenied
from django_graphene_permissions.permissions import IsAuthenticated
from graphene_django import DjangoObjectType

from .email_sendgrid import *
from .models import Category, Community, Event, Speaker, Tag
from .permissions import *
from .schema_community import CategoryType, CommunityType, EventType, TagType


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        kind = graphene.String(required=True)
        address = graphene.String()
        city = graphene.String()
        country = graphene.String()
        live_URL = graphene.String()
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        max_RSVP = graphene.Int()
        community = graphene.ID()
        category = graphene.ID(required=True)
        tags = graphene.List(graphene.String)
        speakers = graphene.List(graphene.ID)

    event = graphene.Field(EventType)
    community = graphene.Field(CommunityType)
    tags = graphene.List(TagType)
    category = graphene.Field(CategoryType)

    @permissions_checker([IsCoreMember])
    def mutate(root, info, **kwargs):
        # print(kwargs)
        community = Community.objects.get(id=kwargs.pop("community"))
        if not check_object_permissions([IsCoreMember], info.context, community):
            raise PermissionDenied()
        category = Category.objects.get(id=kwargs.pop("category"))
        if "speakers" in kwargs.keys():
            speaker_list = kwargs.pop("speakers")
        else:
            speaker_list = []
        # tags = Tag.objects.filter(id__in=kwargs.pop("tags"))
        # tag_obj =
        tags = kwargs.pop("tags")
        print(tags)
        event = Event(**kwargs, community=community, category=category)
        event.save()
        event.refresh_from_db()
        for tag in tags:
            # print(tag)
            tag_obj, created = Tag.objects.get_or_create(name=tag.lower())
            # print(tag_obj.name, created)
            tag_obj.events.add(event)
        for speaker_id in speaker_list:
            if Speaker.objects.get(id=speaker_id):
                event.speakers.add(Speaker.objects.get(id=speaker_id))
        community = event.community
        event.attendees.add(community.leader)
        event.attendees.add(*(community.core_members.all()))
        event.attendees.add(*(community.volunteers.all()))
        event.save()
        # For datetime - https://github.com/graphql-python/graphene/issues/136
        # event.tags.add(*tags)
        # event = Event.objects.get(id=event.id)
        event = Event.objects.get(id=event.id)
        tags = event.tags.all()
        print(tags)
        return CreateEvent(event=event, community=community, category=category, tags=tags)


class Register4Event(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    event = graphene.Field(EventType)

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        id = kwargs.pop("id")
        user = info.context.user
        Event.objects.get(id=id).attendees.add(user)
        event = Event.objects.get(id=id)
        return Register4Event(event=event)


class UnRegister4Event(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    event = graphene.Field(EventType)

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        id = kwargs.pop("id")
        user = info.context.user
        Event.objects.get(id=id).attendees.remove(user)
        event = Event.objects.get(id=id)
        return UnRegister4Event(event=event)


class Checkin4Event(graphene.Mutation):
    class Arguments:
        eventid = graphene.ID(required=True)
        userid = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @permissions_checker([IsVolunteer])
    def mutate(root, info, **kwargs):
        eventid = kwargs.pop("eventid")
        userid = kwargs.pop("userid")
        user = User.objects.get(id=userid)
        event = Event.objects.get(id=eventid)
        if not check_object_permissions([IsVolunteer], info.context, event):
            raise PermissionDenied()
        attends = event.attendees.all()
        if user in attends:
            Event.objects.get(id=eventid).checkins.add(user)
            ok = True
            message = "Successfully Checkedin"
        else:
            ok = False
            message = "User hasn't registered for event"
        return Checkin4Event(ok=ok, message=message)


class Uncheck4Event(graphene.Mutation):
    class Arguments:
        eventid = graphene.ID(required=True)
        userid = graphene.String(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @ permissions_checker([IsVolunteer])
    def mutate(root, info, *args, **kwargs):
        eventid = kwargs.pop("eventid")
        userid = kwargs.pop("userid")
        user = User.objects.get(id=userid)
        event = Event.objects.get(id=eventid)
        if not check_object_permissions([IsVolunteer], info.context, event):
            raise PermissionDenied()
        # user = User.objects.get(kwargs.get(''))
        event.checkins.remove(user)
        return Uncheck4Event(ok=True, message="Checkin removed")


class AddSpeaker(graphene.Mutation):
    class Arguments:
        eventid = graphene.ID(required=True)
        speakerid = graphene.ID(required=True)

    ok = graphene.Boolean()

    @ permissions_checker([IsCoreMember])
    def mutate(root, info, eventid, speakerid):
        event = Event.objects.get(id=eventid)
        if not check_object_permissions([IsCoreMember], info.context, event):
            raise PermissionDenied()
        # user = User.objects.get(kwargs.get(''))
        event.speakers.add(speakerid)
        speaker = Speaker.objects.get(id=speakerid)
        send_speaker_email(speaker.first_name, speaker.email,
                           event.name, event.id, event.community.name)
        return AddSpeaker(ok=True)


class RemoveSpeaker(graphene.Mutation):
    class Arguments:
        eventid = graphene.ID(required=True)
        speakerid = graphene.ID(required=True)

    ok = graphene.Boolean()

    @ permissions_checker([IsCoreMember])
    def mutate(root, info, eventid, speakerid):
        event = Event.objects.get(id=eventid)
        if not check_object_permissions([IsCoreMember], info.context, event):
            raise PermissionDenied()
        # user = User.objects.get(kwargs.get(''))
        event.speakers.remove(speakerid)
        return RemoveSpeaker(ok=True)


# TODO: test
class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        kind = graphene.String()
        address = graphene.String()
        city = graphene.String()
        country = graphene.String()
        live_URL = graphene.String()
        start_time = graphene.DateTime()
        end_time = graphene.DateTime()
        max_RSVP = graphene.Int()
        category = graphene.ID()
        tags = graphene.List(graphene.String)
        speakers = graphene.List(graphene.ID)

    event = graphene.Field(EventType)
    community = graphene.Field(CommunityType)
    tags = graphene.List(TagType)
    category = graphene.Field(CategoryType)

    @ permissions_checker([IsCoreMember])
    def mutate(root, info, **kwargs):
        id = kwargs.pop("id")

        if "speakers" in kwargs.keys():
            speaker_list = kwargs.pop("speakers")
        else:
            speaker_list = []

        try:
            tags = kwargs.pop("tags")

        except Exception:
            pass

        event = Event.objects.get(id=id)
        if not check_object_permissions([IsCoreMember], info.context, event):
            raise PermissionDenied()

        Event.objects.filter(id=id).update(**kwargs)
        event = Event.objects.get(id=id)
        for speaker_id in speaker_list:
            if Speaker.objects.get(id=speaker_id):
                event.speakers.add(Speaker.objects.get(id=speaker_id))

        if tags:
            event.tags.clear()
            for tag in tags:
                # print(tag)
                tag_obj, created = Tag.objects.get_or_create(name=tag.lower())
                # print(tag_obj.name, created)
                tag_obj.events.add(event)
        tags = event.tags.all()
        return UpdateEvent(event=event, community=event.community, tags=tags, category=event.category)
        # category = None
        # try:
        # category_id = kwargs.pop("category")
        # category = Category.objects.get(category_id)
        # except Exception:
        #     pass
        # event = Event.objects.update_or_create(
        #     defaults=kwargs, id=id, category=category
        # )

        # event.save()
        # try:
        #     tags = kwargs.pop("tags")
        #     event.tags.clear()
        #     event.tags.add(*tags)
        # except Exception:
        #     pass
        # # For datetime - https://github.com/graphql-python/graphene/issues/136
        # event.refresh_from_db()
        # community = event.community
        # return UpdateEvent(event=event, community=community, tags=tags, category=category)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @ permissions_checker([IsCoreMember])
    def mutate(root, info, **kwargs):
        obj = Event.objects.get(pk=kwargs["id"])
        if not check_object_permissions([IsCoreMember], info.context, obj):
            raise PermissionDenied()
        obj.delete()
        return DeleteEvent(ok=True)


class UpdateEventImage(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

        # nothing needed for uploading file
     # your return fields
    success = graphene.String()
    picture = graphene.String()

    @permissions_checker([IsCoreMember])
    def mutate(self,  info, id, *args, **kwargs):
        # When using it in Django, context will be the request
        files = info.context.FILES
        event: Event
        event = Event.objects.get(id=id)
        if not check_object_permissions([IsCoreMember], info.context, event):
            raise PermissionDenied()
        event.featured_image = files["file"]
        event.save()
        event = Event.objects.get(id=id)
        return UpdateEventImage(success=True, picture=event.featured_image)


class Query(graphene.ObjectType):
    event_by_id = graphene.Field(EventType, id=graphene.ID())
    events = graphene.List(EventType, kind=graphene.Int(), length=graphene.Int(),
                           filter=graphene.String(), desc=graphene.Boolean())
    events_cat = graphene.List(
        EventType, cat=graphene.ID())
    categories = graphene.List(CategoryType)

    def resolve_event_by_id(root, info, id):
        return Event.objects.get(pk=id)

    def resolve_events(self, info, kind, length, filter, desc):

        filt = "start_time"
        filters = ['start_time', 'end_time', 'creation_time']
        if filter in filters:
            filt = filter
        if desc:
            filt = "-"+filt
        if kind == 0:
            return Event.objects.all().order_by(filt)
        if kind == 1:
            listcom = Event.objects.all().order_by(filt)
            if len(listcom) > length:
                return listcom[:length]
            else:
                return listcom
        else:
            listcom = Event.objects.all().order_by(filt)
            if len(listcom) > length:
                return sample(listcom, length)
            else:
                return listcom

    def resolve_events_cat(root, info, cat):
        print(Category.objects.get(id=cat).event_set.all())
        return Category.objects.get(id=cat).event_set.all()

    def resolve_categories(root, info):
        return Category.objects.all()


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
    checkin_event = Checkin4Event.Field()
    uncheckin_event = Uncheck4Event.Field()
    register_event = Register4Event.Field()
    unregister_event = UnRegister4Event.Field()
    add_speaker = AddSpeaker.Field()
    remove_speaker = RemoveSpeaker.Field()
    update_eventimage = UpdateEventImage.Field()

from .models import Community, Event, Category, Tag
from graphene_django import DjangoObjectType
import graphene
from .schema_community import CommunityType, EventType, CategoryType, TagType
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated


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

    event = graphene.Field(EventType)
    community = graphene.Field(CommunityType)
    tags = graphene.List(TagType)
    category = graphene.Field(CategoryType)

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        # print(kwargs)
        community = Community.objects.get(id=kwargs.pop("community"))
        category = Category.objects.get(id=kwargs.pop("category"))
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
        # For datetime - https://github.com/graphql-python/graphene/issues/136
        # event.tags.add(*tags)
        # event = Event.objects.get(id=event.id)
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


class AddSpeaker(graphene.Mutation):
    class Arguments:
        eventid = graphene.ID(required=True)
        speakerid = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, eventid, speakerid):
        event = Event.objects.get(id=eventid)
        # user = User.objects.get(kwargs.get(''))
        event.speakers.add(speakerid)
        return AddSpeaker(ok=True)


class RemoveSpeaker(graphene.Mutation):
    class Arguments:
        eventid = graphene.ID(required=True)
        speakerid = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, eventid, speakerid):
        event = Event.objects.get(id=eventid)
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

    event = graphene.Field(EventType)
    community = graphene.Field(CommunityType)
    tags = graphene.List(TagType)
    category = graphene.Field(CategoryType)

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        id = kwargs.pop("id")
        try:
            tags = kwargs.pop("tags")

        except Exception:
            pass
        Event.objects.filter(id=id).update(**kwargs)
        event = Event.objects.get(id=id)
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

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        obj = Event.objects.get(pk=kwargs["id"])
        obj.delete()
        return DeleteEvent(ok=True)


class Query(graphene.ObjectType):
    event_by_id = graphene.Field(EventType, id=graphene.ID())
    events = graphene.List(EventType)

    def resolve_event_by_id(root, info, id):
        return Event.objects.get(pk=id)

    def resolve_events(self, info):

        return Event.objects.all().order_by('end_time')


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
    register_event = Register4Event.Field()
    add_speaker = AddSpeaker.Field()
    remove_speaker = RemoveSpeaker.Field()

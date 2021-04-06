from .models import Community, Event, Category, Tag
from graphene_django import DjangoObjectType
import graphene
from .schema_community import CommunityType, EventType, CategoryType, TagType


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
        tags = graphene.List(graphene.ID)

    event = graphene.Field(EventType)
    community = graphene.Field(CommunityType)
    tags = graphene.List(TagType)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        # print(kwargs)
        community = Community.objects.get(id=kwargs.pop("community"))
        category = Category.objects.get(id=kwargs.pop("category"))
        tags = Tag.objects.filter(id__in=kwargs.pop("tags"))
        event = Event(**kwargs, community=community, category=category)
        event.save()
        event.refresh_from_db()  # For datetime - https://github.com/graphql-python/graphene/issues/136
        event.tags.add(*tags)
        return cls(event=event, community=community, category=category, tags=tags)


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
        tags = graphene.List(graphene.ID)

    event = graphene.Field(EventType)
    community = graphene.Field(CommunityType)
    tags = graphene.List(TagType)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop("id")
        category = None
        try:
            category_id = kwargs.pop("category")
            category = Category.objects.get(category_id)
        except Exception:
            pass
        event = Event.objects.update_or_create(
            defaults=kwargs, id=id, category=category
        )

        event.save()
        try:
            tags = kwargs.pop("tags")
            event.tags.clear()
            event.tags.add(*tags)
        event.refresh_from_db()  # For datetime - https://github.com/graphql-python/graphene/issues/136
        community = event.community
        return cls(event=event, community=community, tags=tags, category=category)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Event.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class Query(graphene.ObjectType):
    event_by_id = graphene.Field(EventType, id=graphene.ID())

    def resolve_event_by_id(root, info, id):
        return Event.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()

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
        community = Community.objects.get(id=kwargs.pop('community'))
        category = Category.objects.get(id=kwargs.pop('category'))
        tags = Tag.objects.filter(id__in=kwargs.pop('tags'))
        event = Event(**kwargs, community=community, category=category)
        event.save()
        event.refresh_from_db() # For datetime - https://github.com/graphql-python/graphene/issues/136
        event.tags.add(*tags)
        return cls(event=event, community=community, category=category, tags=tags)



class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from django.forms import ModelForm
from .models import Community, Event, Category, Tag
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import *
from .schema_users import UserType
from django.contrib.auth.models import User
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from random import sample
from .schema_community import EventType, CommunityType


class GeneralSearch(graphene.Mutation):

    class Arguments:
        searchstring = graphene.String(required=True)

    community_list = graphene.List(CommunityType)
    event_list = graphene.List(EventType)

    def mutate(self,  info, *args, **kwargs):
        searchstr = kwargs.pop('searchstring')
        commnity_list = Community.objects.annotate(rank=SearchRank(
            SearchVector('name', 'description', 'address', 'city', 'country'), SearchQuery(searchstr))).order_by('-rank')[:10]
        event_list = Event.objects.annotate(rank=SearchRank(
            SearchVector('name', 'description', 'address', 'city', 'country', 'category__name'), SearchQuery(searchstr))).order_by('-rank')[:10]
        return GeneralSearch(commnity_list, event_list)


class Mutation(graphene.ObjectType):
    general_search = GeneralSearch.Field()

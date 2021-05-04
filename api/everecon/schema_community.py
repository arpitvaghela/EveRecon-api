from random import sample

import graphene
from django.contrib.auth.models import User
from django.forms import ModelForm
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from graphene_django.rest_framework.mutation import SerializerMutation

from .models import Category, Community, Event, Tag
from .schema_users import UserType
from .serializers import *


# Object types
class CommunityType(DjangoObjectType):
    isfollower = graphene.Boolean()
    iscore = graphene.Boolean()
    isvolunteer = graphene.Boolean()

    def resolve_isfollower(parent, info):
        user = info.context.user
        if user in parent.followers.all():
            return True
        else:
            return False

    def resolve_iscore(parent, info):
        user = info.context.user
        if user in parent.core_members.all() or user.id == parent.leader.id:
            return True
        else:
            return False

    def resolve_isvolunteer(parent, info):
        user = info.context.user
        if user in parent.volunteers.all():
            return True
        else:
            return False

    class Meta:
        model = Community


class EventType(DjangoObjectType):
    iscore = graphene.Boolean()
    isvolunteer = graphene.Boolean()
    isregistered = graphene.Boolean()
    ischeckedin = graphene.Boolean()

    def resolve_iscore(parent, info):
        user = info.context.user
        parent: Event
        if user in parent.community.core_members.all() or user.id == parent.community.leader.id:
            return True
        else:
            return False

    def resolve_isvolunteer(parent, info):
        user = info.context.user
        parent: Event
        if user in parent.community.volunteers.all():
            return True
        else:
            return False

    def resolve_isregistered(parent, info):
        user = info.context.user
        parent: Event
        if user in parent.attendees.all():
            return True
        else:
            return False

    def resolve_ischeckedin(parent, info):
        user = info.context.user
        parent: Event
        if user in parent.checkins.all():
            return True
        else:
            return False

    class Meta:
        model = Event


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


# Queries

# Mutations
# Using serializer
# class CreateCommunity(SerializerMutation):
#     class Meta:
#         serializer_class = CommunitySerializer
#         model_operations = ['create', 'update']
#         lookup_field = 'id'

# Using ModelForm
# class CommunityForm(ModelForm):
#     class Meta:
#         model = Community
#         fields = '__all__'


# class CreateCommunity(DjangoFormMutation):
#     community = graphene.Field(CommunityType)

#     class Meta:
#         form_class = CommunityForm


class CreateCommunity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        featured_video = graphene.String()
        address = graphene.String()
        city = graphene.String()
        country = graphene.String()
        email = graphene.String()
        website = graphene.String()
        facebook = graphene.String()
        linkedin = graphene.String()
        twitter = graphene.String()
        instagram = graphene.String()
        discord = graphene.String()
        # leader = graphene.ID(required=True)

    community = graphene.Field(CommunityType)
    leader = graphene.Field(UserType)

    # @classmethod
    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        # leader = User.objects.get(id=kwargs.pop('leader'))
        leader = info.context.user
        community = Community(**kwargs, leader=leader)
        community.save()
        return CreateCommunity(community=community, leader=leader)


class UpdateCommunity(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        featured_video = graphene.String()
        address = graphene.String()
        city = graphene.String()
        country = graphene.String()
        email = graphene.String()
        website = graphene.String()
        facebook = graphene.String()
        linkedin = graphene.String()
        instagram = graphene.String()
        discord = graphene.String()
        is_active = graphene.Boolean()
        followers = graphene.List(graphene.ID)

    community = graphene.Field(CommunityType)
    # followers = graphene.Field(UserType) # TODO: Check if this is required

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        id = kwargs.pop("id")
        followers = None
        try:
            followers = kwargs.pop("followers")
        except Exception:
            pass
        # community = Community.objects.get(id=id)
        # for k, v in kwargs.items():
        #     community.k = v
        # community.save()
        # print(followers)
        # community = Community.objects.filter(id=id).update(**kwargs)
        # community, created = Community.objects.update_or_create(
        #     defaults=kwargs, id=id)
        Community.objects.filter(id=id).update(**kwargs)
        community = Community.objects.get(id=id)
        # print(community.name)
        if followers:
            community.followers.add(*followers)
        # print(community.followers.all())
        return UpdateCommunity(community=community)


class DeleteCommunity(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        obj = Community.objects.get(pk=kwargs["id"])
        obj.delete()
        return DeleteCommunity(ok=True)


class AddCoreMember(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        # user = User.objects.get(kwargs.get(''))
        community.core_members.add(kwargs.get("user"))
        return AddCoreMember(ok=True)


class RemoveCoreMember(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        community.core_members.remove(kwargs.get("user"))
        return RemoveCoreMember(ok=True)


class AddVolunteer(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        # user = User.objects.get(kwargs.get(''))
        community.volunteers.add(kwargs.get("user"))
        return AddVolunteer(ok=True)


class RemoveVolunteer(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        community.volunteers.remove(kwargs.get("user"))
        return RemoveVolunteer(ok=True)


class AddFollower(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        # user = User.objects.get(kwargs.get(''))
        community.followers.add(kwargs.get("user"))
        return AddFollower(ok=True)


class RemoveFollower(graphene.Mutation):
    class Arguments:
        community = graphene.ID(required=True)
        user = graphene.ID(required=True)

    ok = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        community = Community.objects.get(id=kwargs.get("community"))
        community.followers.remove(kwargs.get("user"))
        return RemoveFollower(ok=True)


class UpdateCommunityLogo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

        # nothing needed for uploading file
     # your return fields
    success = graphene.String()
    logo = graphene.String()

    def mutate(self,  info, id, *args, **kwargs):
        # When using it in Django, context will be the request
        files = info.context.FILES
        community: Community
        community = Community.objects.get(id=id)
        print(community)
        community.logo = files["file"]
        community.save()
        community = Community.objects.get(id=id)
        return UpdateCommunityLogo(success=True, logo=community.logo)


class UpdateCommunityBanner(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

        # nothing needed for uploading file
     # your return fields
    success = graphene.String()
    banner = graphene.String()

    def mutate(self,  info, id, *args, **kwargs):
        # When using it in Django, context will be the request
        files = info.context.FILES
        community: Community
        community = Community.objects.get(id=id)
        print(community)
        community.banner = files["file"]
        community.save()
        community = Community.objects.get(id=id)
        return UpdateCommunityBanner(success=True, banner=community.banner)


# Query Class
class Query(graphene.ObjectType):
    community_by_id = graphene.Field(CommunityType, id=graphene.ID())
    # returns all communities or x communities or x sampeled communities
    community_list = graphene.List(CommunityType, kind=graphene.Int(
    ), length=graphene.Int(), filter=graphene.String(), desc=graphene.Boolean())

    def resolve_community_by_id(root, info, id):
        return Community.objects.get(pk=id)

    def resolve_community_list(root, info, kind, length, filter, desc):
        filt = "creation_time"
        filters = ['creation_time', 'members_count']
        if filter in filters:
            filt = filter
        if desc:
            filt = "-"+filt

        if kind == 0:
            return Community.objects.all().order_by(filt)
        if kind == 1:
            listcom = Community.objects.all().order_by(filt)
            if len(listcom) > length:
                return listcom[:length]
            else:
                return listcom
        else:
            listcom = Community.objects.all().order_by(filt)
            if len(listcom) > length:
                return sample(listcom, length)
            else:
                return listcom


class Mutation(graphene.ObjectType):
    create_community = CreateCommunity.Field()
    update_community = UpdateCommunity.Field()
    # create_update_community = CreateCommunity.Field()
    delete_community = DeleteCommunity.Field()

    add_core_member = AddCoreMember.Field()
    remove_core_member = RemoveCoreMember.Field()
    add_volunteer = AddVolunteer.Field()
    remove_volunteer = RemoveVolunteer.Field()
    add_follower = AddFollower.Field()
    remove_follower = RemoveFollower.Field()
    update_communitylogo = UpdateCommunityLogo.Field()
    update_communitybanner = UpdateCommunityBanner.Field()

import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from everecon.models import Profile, User
from graphql_jwt.shortcuts import create_refresh_token, get_token
import graphene
import graphql_jwt
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated

# Mutation: Create User
# We want to return:
# - The new `user` entry
# - The new associated `profile` entry - from our extended model
# - The access_token (so that we're automatically logged in)
# - The refresh_token (so that we can refresh my access token)

# Make models available to graphene.Field


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfile(DjangoObjectType):
    class Meta:
        model = Profile


# CreateUser


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    profile = graphene.Field(UserProfile)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        contact = graphene.String()
        city = graphene.String()
        country = graphene.String()

    def mutate(self, info, username, password, email, **kwargs):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        for i in kwargs.keys():
            setattr(profile_obj, i, kwargs[i])
        profile_obj.save()
        token = get_token(user)

        refresh_token = create_refresh_token(user)
        user = User.objects.get(id=user.id)

        return CreateUser(
            user=user, profile=profile_obj, token=token, refresh_token=refresh_token
        )


class UpdateProfilePicture(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

        # nothing needed for uploading file
     # your return fields
    success = graphene.String()
    picture = graphene.String()

    def mutate(self,  info, id, *args, **kwargs):
        # When using it in Django, context will be the request
        files = info.context.FILES
        profile = User.objects.get(id=id).profile
        profile.profile_picture = files["file"]
        profile.save()
        profile = User.objects.get(id=id).profile
        # print(profile.profile_picture)
        # Or, if used in Flask, context will be the flask global request
        # files = context.files
        # do something with files
        return UpdateProfilePicture(success=True, picture=profile.profile_picture.url)

# Finalize creating mutation for schema


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profpic = UpdateProfilePicture.Field()


# Query: Find users / my own profile
# Demonstrates auth block on seeing all user - only if I'm a manager
# Demonstrates auth block on seeing myself - only if I'm logged in


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)
    myprofile = graphene.Field(UserType)
    # users = graphene.List(UserType)

    @permissions_checker([IsAuthenticated])
    def resolve_whoami(self, info):
        user = info.context.user
        # Check to to ensure you're signed-in to see yourself
        return user

    @permissions_checker([IsAuthenticated])
    def resolve_myprofile(self, info):
        user = info.context.user
        # Check to to ensure you're signed-in to see yourself
        return user
    # def resolve_users(self, info):
    #     user = info.context.user
    #     print(user)
    #     # Check to ensure user is a 'manager' to see all users
    #     if user.is_anonymous:
    #         raise Exception('Authentication Failure: Your must be signed in')
    #     if user.profile.role != 'manager':
    #         raise Exception('Authentication Failure: Must be Manager')
    #     return get_user_model().objects.all()

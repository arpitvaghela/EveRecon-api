import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from everecon.models import Profile, User
from graphene_django import DjangoObjectType
from graphql_jwt.shortcuts import create_refresh_token, get_token

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


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

# CreateUser


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    profile = graphene.Field(ProfileType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        firstname = graphene.String()
        lastname = graphene.String()
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
        fname = kwargs.pop("firstname")
        lname = kwargs.pop("lastname")
        user.first_name = fname
        user.last_name = lname
        # print(user.firstName)
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
        return UpdateProfilePicture(success=True, picture=profile.profile_picture.url)

# Finalize creating mutation for schema


class UpdateProfile(graphene.Mutation):
    class Arguments:
        firstname = graphene.String()
        lastname = graphene.String()
        contact = graphene.String()
        city = graphene.String()
        country = graphene.String()

    profile = graphene.Field(ProfileType)
    user = graphene.Field(UserType)

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
        user = info.context.user
        profile_obj = user.profile
        fname = kwargs.pop("firstname")
        lname = kwargs.pop("lastname")
        user: User
        user.first_name = fname
        user.last_name = lname
        user.save()
        for i in kwargs.keys():
            setattr(profile_obj, i, kwargs[i])
        profile_obj.save()
        profile_obj = User.objects.get(id=user.id).profile
        user = User.objects.get(id=user.id)
        return UpdateProfile(profile=profile_obj, user=user)


class UpdateUserSecurity(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
    user = graphene.Field(UserType)

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
        user = info.context.user
        email = kwargs.pop("email")
        pwd = kwargs.pop("password")
        user: User
        user.email = email
        user.set_password(pwd)
        user.save()
        user = User.objects.get(id=user.id)
        return UpdateUserSecurity(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profpic = UpdateProfilePicture.Field()
    update_user = UpdateProfile.Field()
    update_usersecurity = UpdateUserSecurity.Field()


# Query: Find users / my own profile
# Demonstrates auth block on seeing all user - only if I'm a manager
# Demonstrates auth block on seeing myself - only if I'm logged in


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)
    myprofile = graphene.Field(UserType)
    user_by_name = graphene.Field(UserType, username=graphene.String())
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

    # @permissions_checker([IsAuthenticated])
    def resolve_user_by_name(self, info, username):
        user = User.objects.get(username=username)
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

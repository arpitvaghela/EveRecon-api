from .models import Profile, User
from graphene_django import DjangoObjectType
import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UpdateProfile(graphene.Mutation):
    class Arguments:
        contact = graphene.String()
        city = graphene.String()
        country = graphene.String()
        user = graphene.ID(required=True)

    profile = graphene.Field(ProfileType)
    user = graphene.Field(UserType)

    @classmethod
    @permissions_checker([IsAuthenticated])
    def mutate(cls, root, info, **kwargs):
        pass

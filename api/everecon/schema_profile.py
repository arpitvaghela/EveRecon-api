from .models import Profile, User
from graphene_django import DjangoObjectType
import graphene


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
    def mutate(cls, root, info, **kwargs):
        pass

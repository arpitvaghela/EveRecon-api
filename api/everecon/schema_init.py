import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene import ObjectType
from graphene_django import DjangoObjectType


class Query(ObjectType):

    foo = graphene.String()

    @permissions_checker([IsAuthenticated])
    def resolve_foo(root, info, **kwargs):
        return "Hello, World!"

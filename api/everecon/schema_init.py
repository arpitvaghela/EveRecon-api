import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType


class Query(ObjectType):

    foo = graphene.String()

    def resolve_foo(root, info, **kwargs):
        return "Hello, World!"

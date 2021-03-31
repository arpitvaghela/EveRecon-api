import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from django.forms import ModelForm
from everecon.models import Community
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import *
# Object types
class CommunityType(DjangoObjectType):
    class Meta:
        model = Community

# Queries

# Mutations

class CreateCommunity(SerializerMutation):
    class Meta:
        serializer_class = CommunitySerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'

# class CommunityForm(ModelForm):
#     class Meta:
#         model = Community
#         fields = '__all__'


# class CreateCommunity(DjangoFormMutation):
#     community = graphene.Field(CommunityType)

#     class Meta:
#         form_class = CommunityForm

class DeleteCommunity(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Community.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)

# Query Class
class Query(graphene.ObjectType):
    community_by_id = graphene.Field(CommunityType, id=graphene.Int())

    def resolve_community_by_id(root, info, id):
        return Community.objects.get(pk=id)

# Mutation Class
class Mutation(graphene.ObjectType):
    create_update_community = CreateCommunity.Field()
    delete_community = DeleteCommunity.Field()

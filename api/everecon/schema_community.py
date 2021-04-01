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
    
    community = graphene.Field(CommunityType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        community = Community(**kwargs)
        community.save()
        return cls(community=community)

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

    community = graphene.Field(CommunityType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop('id')
        community = Community.objects.get(id=id)
        for k, v in kwargs.items():
            community.k = v
        community.save()
        return cls(community=community)

class DeleteCommunity(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

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
    create_community = CreateCommunity.Field()
    update_community = UpdateCommunity.Field()
    # create_update_community = CreateCommunity.Field()
    delete_community = DeleteCommunity.Field()

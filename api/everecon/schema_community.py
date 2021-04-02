import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from django.forms import ModelForm
from everecon.models import Community
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import *
from .schema_event import EventType
from .schema_users import UserType
from django.contrib.auth.models import User

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
        creator = graphene.ID(required=True)        
    
    community = graphene.Field(CommunityType)
    creator = graphene.Field(UserType)
    
    @classmethod
    def mutate(cls, root, info, **kwargs):
        creator = User.objects.get(id=kwargs.get('creator'))
        community = Community(**kwargs, creator=creator)
        community.save()
        return cls(community=community, creator=creator)

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

    @classmethod
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop('id')
        followers = None
        try:
            followers = kwargs.pop('followers')            
        except IndexError:
            pass
        # print(followers)
        community = Community.objects.get(id=id)
        for k, v in kwargs.items():
            community.k = v
        community.save()
        if followers:
            community.followers.add(*followers)
        # print(community.followers.all())
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

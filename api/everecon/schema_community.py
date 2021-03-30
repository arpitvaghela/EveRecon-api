import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from django.forms import ModelForm
from everecon.models import Community

# Object types
class CommunityType(DjangoObjectType):
    class Meta:
        model = Community

# Queries

# Mutations
class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = '__all__'


class CreateCommunity(DjangoFormMutation):
    community = graphene.Field(CommunityType)

    class Meta:
        form_class = CommunityForm

# Query Class
class Query(graphene.ObjectType):
    pass

# Mutation Class
class Mutation(graphene.ObjectType):
    create_community = CreateCommunity.Field()


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

    # name = models.CharField(max_length=255)
    # description = models.TextField(blank=True) # Not setting null=True as a Community must have a description
    # logo = models.ImageField(upload_to='images/community/logos/', null=True, blank=True)
    # banner = models.ImageField(upload_to='images/community/banners/', null=True, blank=True)
    # featured_video = models.URLField(blank=True, null=True) # TODO: Add a validation for YouTube URL
    # # featured_video = models.FileField(upload_to='videos/community/featured/', blank=True, null=True, verbose_name="")
    # events = models.ManyToManyField(Event, related_name="communities", blank=True)
    # address = models.TextField(null=True, blank=True)
    # city = models.CharField(max_length=255, null=True, blank=True)
    # country = models.CharField(max_length=255, null=True, blank=True)
    # email = models.EmailField(null=True, blank=True)
    # members_count = models.IntegerField(blank=True, default=0) # TODO: Update this automatically
    # website = models.URLField(null=True, blank=True)
    # facebook = models.URLField(null=True, blank=True) # TODO: Validation for social media
    # linkedin = models.URLField(null=True, blank=True)
    # twitter = models.URLField(null=True, blank=True)
    # instagram = models.URLField(null=True, blank=True)
    # discord = models.URLField(null=True, blank=True)
    # is_active = models.BooleanField(default=True)
    # creation_time = models.TimeField(auto_now_add=True, blank=True)
    # followers = models.ManyToManyField(User ,related_name="communities", blank=True)

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

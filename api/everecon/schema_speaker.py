from .models import Speaker
from graphene_django import DjangoObjectType
import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated


class SpeakerType(DjangoObjectType):
    class Meta:
        model = Speaker


class CreateSpeaker(graphene.Mutation):
    class Arguments():
        first_name = graphene.String(required=True)
        last_name = graphene.String()
        email = graphene.String()
        facebook = graphene.String()
        instagram = graphene.String()
        profile_picture = models.ImageField(
            upload_to="images/speaker/speaker_profile_pictures/", blank=True, null=True
        )
        description = graphene.String()
    speaker = graphene.field(SpeakerType)

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        speaker = Speaker(**kwargs)
        speaker.save()
        return CreateSpeaker(community=speaker)


class Query(graphene.ObjectType):
    speaker_by_email = graphene.Field(SpeakerType, email=graphene.String())
    all_speaker = graphene.List(SpeakerType)

    def resolve_speaker_by_email(root, info, email):
        return Speaker.objects.get(email=email)

    def resolve_all_speaker(root, info):
        return Speaker.objects.all()


class Mutation(graphene.ObjectType):
    create_speaker = CreateSpeaker.Field()

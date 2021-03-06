import graphene
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from graphene_django import DjangoObjectType

from .models import Speaker


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
        description = graphene.String()

    speaker = graphene.Field(SpeakerType)

    @permissions_checker([IsAuthenticated])
    def mutate(root, info, **kwargs):
        speaker = Speaker(**kwargs)
        speaker.save()
        return CreateSpeaker(speaker=speaker)


class UpdateSpeakerPicture(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

        # nothing needed for uploading file
     # your return fields
    success = graphene.String()
    picture = graphene.String()
    
    @permissions_checker([IsAuthenticated])
    def mutate(self,  info, id, *args, **kwargs):
        # When using it in Django, context will be the request
        files = info.context.FILES
        speaker = Speaker.objects.get(id=id)
        speaker.profile_picture = files["file"]
        speaker.save()
        speaker = Speaker.objects.get(id=id)
        return UpdateSpeakerPicture(success=True, picture=speaker.profile_picture.url)


class Query(graphene.ObjectType):
    speaker_by_email = graphene.Field(SpeakerType, email=graphene.String())
    all_speaker = graphene.List(SpeakerType)

    def resolve_speaker_by_email(root, info, email):
        return Speaker.objects.get(email=email)

    def resolve_all_speaker(root, info):
        return Speaker.objects.all()


class Mutation(graphene.ObjectType):
    create_speaker = CreateSpeaker.Field()
    update_speakerpicture = UpdateSpeakerPicture.Field()

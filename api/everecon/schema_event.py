from everecon.models import Community
from graphene_django import DjangoObjectType

class EventType(DjangoObjectType):
    class Meta:
        model = Community

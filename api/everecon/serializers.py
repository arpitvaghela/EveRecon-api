from rest_framework import serializers
from .models import Community
from django.http import Http404

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        if 'id' in input:
            instance = Community.objects.get(id=input['id'])
            if instance:
                return {'instance': instance, 'data': input, 'partial': True}
            else:
                raise Http404

        return {'data': input, 'partial': True}

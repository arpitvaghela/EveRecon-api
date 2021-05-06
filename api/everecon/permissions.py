from django_graphene_permissions.permissions import BasePermission
from .models import Community, Event

class IsCommunityLeader(BasePermission):
    @staticmethod
    def has_permission(context):
        return context.user and context.user.is_authenticated

    @staticmethod
    def has_object_permission(context, obj):
        if isinstance(obj,Event):
            obj = obj.community
        return context.user == obj.leader

class IsCoreMember(BasePermission):
    @staticmethod
    def has_permission(context):
        return context.user and context.user.is_authenticated

    @staticmethod
    def has_object_permission(context, obj):
        if isinstance(obj,Event):
            obj = obj.community
        return context.user in obj.core_members.all() or context.user == obj.leader

class IsVolunteer(BasePermission):
    @staticmethod
    def has_permission(context):
        return context.user and context.user.is_authenticated

    @staticmethod
    def has_object_permission(context, obj):
        if isinstance(obj,Event):
            obj = obj.community
        return context.user in obj.volunteers.all() or context.user in obj.core_members.all() or context.user == obj.leader

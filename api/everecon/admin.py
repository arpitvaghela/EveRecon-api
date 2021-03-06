from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Category, Community, Event, Tag, Profile, Speaker

# Register your models here.
# Inline + descriptor


class AdminProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"


# Define new admin with inline


class ProfileUserAdmin(BaseUserAdmin):
    inlines = (AdminProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, ProfileUserAdmin)
admin.site.register(Community)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Speaker)

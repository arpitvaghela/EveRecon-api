from uuid import uuid4
import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models.signals import pre_save
import inspect
import sys


# Validation for facebook handle URL
def validation_facebook(facebook):
    url_validator_message = "Invalid handle URL!"
    facebook_regex = "/(?:(?:http|https):\/\/)?(?:www\.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?"
    url_validator = RegexValidator(
        regex=facebook_regex, message=url_validator_message)
    return url_validator(facebook)


# Validation for instagram handle URL
def validation_instagram(instagram):
    url_validator_message = "Invalid handle URL!"
    instagram_regex = "/(?:(?:http|https):\/\/)?(?:www\.)?(?:instagram\.com|instagr\.am)\/([A-Za-z0-9-_\.]+)?"
    url_validator = RegexValidator(
        regex=instagram_regex, message=url_validator_message)
    return url_validator(instagram)


# Validation for twitter handle URL
def validation_twitter(twitter):
    url_validator_message = "Invalid handle URL!"
    twitter_regex = "/(?:(?:http|https):\/\/)?(?:www\.)?twitter\.com\/([a-zA-Z0-9_]+)?"
    url_validator = RegexValidator(
        regex=twitter_regex, message=url_validator_message)
    return url_validator(twitter)


# Validation for linkedin handle URL
def validation_linkedin(linkedin):
    url_validator_message = "Invalid handle URL!"
    linkedin_regex = "/(?:(?:http|https):\/\/)?(?:www\.)?linkedin.com/((in/[^/]+/?)|(pub/[^/]+/((\w|\d)+/?){3}))$"
    url_validator = RegexValidator(
        regex=linkedin_regex, message=url_validator_message)
    return url_validator(linkedin)


# Validation for discord handle URL
def validation_discord(discord):
    url_validator_message = "Invalid handle URL!"
    discord_regex = "(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/users)\/.{3,32}#[0-9]{4}"
    url_validator = RegexValidator(
        regex=discord_regex, message=url_validator_message)
    return url_validator(discord)


# Validation for facebook handle URL
def validation_youtube(youtube):
    url_validator_message = "Invalid handle URL!"
    youtube_regex = "/(?:(?:http|https):\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
    url_validator = RegexValidator(
        regex=youtube_regex, message=url_validator_message)
    return url_validator(youtube)


def path_and_rename_profile(instance, filename):
    upload_to = 'profiles'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename_event(instance, filename):
    upload_to = 'events'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename_communitylogo(instance, filename):
    upload_to = 'communitylogo'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_and_rename_communitybanner(instance, filename):
    upload_to = 'communitybanner'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# User Model, using Django's inbuilt model for now so ignore this
# class User(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     firstName = models.CharField(max_length=255)
#     lastName = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     emailId = models.EmailField(max_length=255, unique=True)
#     contact = models.CharField(max_length=15)
#     profilePicture = models.ImageField(upload_to='images/')
#     city = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     creationTime = models.TimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.username


class Profile(models.Model):
    contact = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=path_and_rename_profile, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    TYPE_CHOICES = [
        ("V", "Virtual"),
        ("P", "In-Person"),
    ]
    kind = models.CharField(
        max_length=255, choices=TYPE_CHOICES
    )  # Type should have options
    address = models.TextField(null=True, blank=True)
    city = models.CharField(
        max_length=255, null=True, blank=True
    )  # Needs to be discussed
    country = models.CharField(max_length=255, null=True, blank=True)
    # Either of the two must be there
    live_URL = models.URLField(null=True, blank=True)
    # category = models.CharField(max_length=255)
    # tags = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    # attendees = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(
        upload_to=path_and_rename_event, null=True, blank=True
    )
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.TimeField(auto_now_add=True, blank=True)
    max_RSVP = models.IntegerField(default=300)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="events")
    attendees = models.ManyToManyField(
        User, related_name="events_attended", blank=True)
    checkins = models.ManyToManyField(
        User, related_name="events_checkedin", blank=True)
    speakers = models.ManyToManyField(
        "Speaker", related_name="events", blank=True)
    community = models.ForeignKey(
        "Community", on_delete=models.CASCADE, related_name="events"
    )

    def __str__(self):
        return self.name


class Speaker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    facebook = models.URLField()
    instagram = models.URLField()
    profile_picture = models.ImageField(
        upload_to=path_and_rename_profile, blank=True, null=True
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True
    )  # Not setting null=True as a Community must have a description
    logo = models.ImageField(
        upload_to=path_and_rename_communitybanner, null=True, blank=True)
    banner = models.ImageField(
        upload_to=path_and_rename_communitylogo, null=True, blank=True
    )
    featured_video = models.URLField(
        blank=True, null=True, validators=[validation_youtube]
    )
    # featured_video = models.FileField(upload_to='videos/community/featured/', blank=True, null=True, verbose_name="")
    # events = models.ManyToManyField(Event, related_name="communities", blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    members_count = models.IntegerField(
        blank=True, default=0
    )  # TODO: Update this automatically
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(
        null=True, blank=True, validators=[validation_facebook])
    linkedin = models.URLField(
        null=True, blank=True, validators=[validation_linkedin])
    twitter = models.URLField(null=True, blank=True,
                              validators=[validation_twitter])
    instagram = models.URLField(
        null=True, blank=True, validators=[validation_instagram]
    )
    discord = models.URLField(null=True, blank=True,
                              validators=[validation_discord])
    is_active = models.BooleanField(default=True)
    creation_time = models.TimeField(auto_now_add=True, blank=True)
    followers = models.ManyToManyField(
        User, related_name="communities", blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    core_members = models.ManyToManyField(
        User, related_name="communities_core_members", blank=True
    )
    volunteers = models.ManyToManyField(
        User, related_name="communities_volunteers", blank=True
    )

    def __str__(self):
        return self.name


@receiver(post_save, sender=Community)
def save_user_profile(sender, instance, **kwargs):
    instance: Community
    instance.members_count = instance.members_count+1
    instance.save()


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(
        upload_to="images/sponsor/logos/", null=True, blank=True)
    banner = models.ImageField(
        upload_to="images/community/banners/", null=True, blank=True
    )
    communities = models.ManyToManyField(
        Community, related_name="sponsors", blank=True
    )  # Sponsors sponsor communities, not events

    def __str__(self):
        return self.name


MODELS = [obj for name, obj in
          inspect.getmembers(sys.modules[__name__], inspect.isclass)]


def validate_model(sender, instance, **kwargs):
    if 'raw' in kwargs and not kwargs['raw']:
        if type(instance) in MODELS:
            instance.full_clean()


pre_save.connect(validate_model, dispatch_uid='validate_models')


# class CommunityLeader(models.Model):
#     creation_time = models.TimeField(auto_now_add=True, blank=True)
#     communities = models.ManyToManyField(Community, related_name="community_leaders", blank=True)
#     users = models.ManyToManyField(User, related_name="community_leaders_at", blank=True)

# class CoreMember(models.Model):
#     creation_time = models.TimeField(auto_now_add=True, blank=True)
#     communities = models.ManyToManyField(Community, related_name="core_members", blank=True)
#     users = models.ManyToManyField(User, related_name="core_members_at", blank=True)


# class Member(models.Model):
#     creation_time = models.TimeField(auto_now_add=True, blank=True)
#     communities = models.ManyToManyField(Community, related_name="members", blank=True)
#     users = models.ManyToManyField(User, related_name="members_at", blank=True)


# class Volunteer(models.Model):
#     creation_time = models.TimeField(auto_now_add=True, blank=True)
#     communities = models.ManyToManyField(Community, related_name="volunteers", blank=True)
#     users = models.ManyToManyField(User, related_name="volunteers_at", blank=True)

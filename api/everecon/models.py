from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone, dateformat
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    profile_picture = models.ImageField(upload_to='images/', null=True, blank=True)
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
    description = models.TextField(null=True,blank=True)
    type = models.CharField(max_length=255) # Type should have options
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True) # Needs to be discussed
    country = models.CharField(max_length=255, null=True, blank=True)
    live_URL = models.URLField(null=True, blank=True) # Either of the two must be there
    # category = models.CharField(max_length=255)
    # tags = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # attendees = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='images/event/featured/', null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    creation_time = models.TimeField(auto_now_add=True, blank=True)
    max_RSVP = models.IntegerField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    attendees = models.ManyToManyField(User, related_name="events_attended", blank=True)
    speakers = models.ManyToManyField('Speaker', related_name="events", blank=True)

    def __str__(self):
        return self.name

class Speaker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    facebook = models.URLField()
    instagram = models.URLField()
    profile_picture = models.ImageField(upload_to='images/speaker/profile_pictures/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True) # Not setting null=True as a Community must have a description
    logo = models.ImageField(upload_to='images/community/logos/', null=True)
    banner = models.ImageField(upload_to='images/community/banners/', null=True, blank=True)
    featured_video = models.URLField(blank=True, null=True) # TODO: Add a validation for YouTube URL
    # featured_video = models.FileField(upload_to='videos/community/featured/', blank=True, null=True, verbose_name="")
    events = models.ManyToManyField(Event, related_name="communities", blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    members_count = models.IntegerField() # TODO: Update this automatically
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True) # TODO: Validation for social media
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    discord = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    creation_time = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='images/sponsor/logos/', null=True, blank=True)
    banner = models.ImageField(upload_to='images/community/banners/', null=True, blank=True)
    communities = models.ManyToManyField(Community, related_name='sponsors', blank=True) # Sponsors sponsor communities, not events

    def __str__(self):
        return self.name

class CommunityLeader(models.Model):
    creation_time = models.TimeField(auto_now_add=True, blank=True)
    communities = models.ManyToManyField(Community, related_name="community_leaders", blank=True)
    users = models.ManyToManyField(User, related_name="community_leaders_at", blank=True)

class CoreMember(models.Model):
    creation_time = models.TimeField(auto_now_add=True, blank=True)
    communities = models.ManyToManyField(Community, related_name="core_members", blank=True)
    users = models.ManyToManyField(User, related_name="core_members_at", blank=True)

class Member(models.Model):
    creation_time = models.TimeField(auto_now_add=True, blank=True)
    communities = models.ManyToManyField(Community, related_name="members", blank=True)
    users = models.ManyToManyField(User, related_name="members_at", blank=True)

class Volunteer(models.Model):
    creation_time = models.TimeField(auto_now_add=True, blank=True)
    communities = models.ManyToManyField(Community, related_name="volunteers", blank=True)
    users = models.ManyToManyField(User, related_name="volunteers_at", blank=True)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone, dateformat


# User Model
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


# Profile Model
class Profile(models.Model):
    contact = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='images/')
    user = models.OneToOneField(User, on_delete=models.CASCADE())

    def __str__(self):
        return self.user.__str__()


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    live_URL = models.URLField(blank=True, editable=True)
    category = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    attendees = models.ForeignKey(User, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)
    creation_time = models.TimeField(auto_now_add=True)
    max_RSVP = models.IntegerField()

    def __str__(self):
        return self.name


# Community model
class Community:
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='images/')
    banner = models.ImageField(upload_to='images/', blank=True)
    featuredVideo = models.FileField(upload_to='videos/', null=True, verbose_name="")
    address = models.TextField(blank=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    liveURL = models.URLField(blank=True, editable=True)
    category = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    startTime = models.TimeField()
    endTime = models.TimeField()
    attendees = models.ForeignKey(User, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='images/')
    isActive = models.BooleanField(default=True)
    creationTime = models.TimeField(auto_now_add=True)
    maxRSVP = models.IntegerField(max_length=255)


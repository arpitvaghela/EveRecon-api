# Generated by Django 3.1.2 on 2021-04-04 07:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('everecon', '0006_auto_20210403_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='communities',
        ),
        migrations.RemoveField(
            model_name='member',
            name='users',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='communities',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='users',
        ),
        migrations.AddField(
            model_name='community',
            name='core_members',
            field=models.ManyToManyField(blank=True, related_name='communities_core_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='community',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='communities_volunteers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CoreMember',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='Volunteer',
        ),
    ]

# Generated by Django 3.1.2 on 2021-04-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everecon', '0007_auto_20210404_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('V', 'Virtual'), ('P', 'In-Person')], max_length=255),
        ),
    ]
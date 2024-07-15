# Generated by Django 5.0.6 on 2024-07-15 10:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_image_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='facebook',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='img/profile/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-06 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0007_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='twitter_access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_access_token_secret',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

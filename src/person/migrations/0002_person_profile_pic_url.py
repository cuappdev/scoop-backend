# Generated by Django 4.0.2 on 2022-03-17 22:15

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="profile_pic_url",
            field=models.TextField(default=None, null=True),
        ),
    ]

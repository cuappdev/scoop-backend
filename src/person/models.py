from django.contrib.auth.models import User
from django.db import models
from prompts.models import Prompt


class Person(models.Model):
    netid = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=20, null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, default=None
    )
    grade = models.CharField(max_length=20, default=None, null=True)
    profile_pic_url = models.TextField(default=None, null=True)
    pronouns = models.CharField(max_length=20, default=None, null=True)
    prompt_questions = models.ManyToManyField(Prompt, default=None, blank=True)
    prompt_answers = models.TextField(default=None, null=True)

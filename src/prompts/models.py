from django.db import models

class Prompt(models.Model):
    question_name = models.CharField(max_length=200)
    question_placeholder = models.CharField(max_length=200, default="", null=True)


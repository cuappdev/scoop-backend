from prompts.models import Prompt
from rest_framework import serializers


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ("id", "question_name", "question_placeholder")
        read_only_fields = fields
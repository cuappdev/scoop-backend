import json

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Person


class SimplePersonSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    prompts = SerializerMethodField("get_prompts")

    class Meta:
        model = Person
        fields = (
            "id",
            "netid",
            "first_name",
            "last_name",
            "profile_pic_url",
            "grade",
            "pronouns",
            "prompts",
        )
        read_only_fields = fields

    def get_prompts(self, person):
        prompt_questions = sorted(person.prompt_questions.all(), key=lambda x: x.id)
        prompt_answers = person.prompt_answers
        if prompt_answers is None:
            return []
        prompt_answers = json.loads(prompt_answers)
        prompts = []
        for i in range(len(prompt_questions)):
            prompts.append(
                {
                    "id": prompt_questions[i].id,
                    "question_name": prompt_questions[i].question_name,
                    "question_placeholder": prompt_questions[i].question_placeholder,
                    "answer": prompt_answers[i],
                }
            )
        return prompts

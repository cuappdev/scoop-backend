import json

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from ride.simple_serializers import SimpleRideSerializer


class AuthenticateSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField(method_name="get_access_token")

    class Meta:
        model = User
        fields = (
            "access_token",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = fields

    def get_access_token(self, instance):
        return self.context.get("access_token")


class UserSerializer(serializers.ModelSerializer):
    netid = serializers.CharField(source="person.netid")
    grade = serializers.CharField(source="person.grade")
    pronouns = serializers.CharField(source="person.pronouns")
    profile_pic_url = serializers.CharField(source="person.profile_pic_url")
    phone_number = serializers.CharField(source="person.phone_number")
    prompts = SerializerMethodField("get_prompts")
    rides = SerializerMethodField("get_rides")

    def get_prompts(self, user):
        prompt_questions = user.person.prompt_questions.all()
        prompt_answers = user.person.prompt_answers
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

    def get_rides(self, user):
        active_rides = set()
        rides = (
            user.person.driver.all()
            | user.person.ride_set.all()
            | user.person.creator.all()
        )
        rides = sorted(rides, key=lambda ride: ride.id)
        for ride in rides:
            if ride.departure_datetime >= timezone.now():
                active_rides.add(ride)
            else:
                ride.delete()
        return [SimpleRideSerializer(ride).data for ride in active_rides]

    class Meta:
        model = User
        fields = (
            "id",
            "netid",
            "first_name",
            "last_name",
            "phone_number",
            "grade",
            "profile_pic_url",
            "pronouns",
            "prompts",
            "rides",
        )
        read_only_fields = fields

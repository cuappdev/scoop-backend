from django.contrib.auth.models import User
from rest_framework import serializers


class AuthenticateSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField(method_name="get_access_token")

    class Meta:
        model = User
        fields = (
            "access_token",
            User.USERNAME_FIELD,
            "first_name",
            "last_name",
        )
        read_only_fields = fields

    def get_access_token(self, instance):
        return self.context.get("access_token")


class UserSerializer(serializers.ModelSerializer):
    netid = serializers.CharField(source="person.netid")
    grade = serializers.CharField(source="person.graduation_year")
    pronouns = serializers.CharField(source="person.pronouns")
    phone_number = serializers.CharField(source="person.has_onboarded")

    class Meta:
        model = User
        fields = (
            "id",
            "netid",
            "first_name",
            "last_name",
            "phone_number",
            "grade",
            "pronouns",
        )
        read_only_fields = fields

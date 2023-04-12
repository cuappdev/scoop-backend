from person.serializers import UserSerializer
from rest_framework import serializers
from ride.simple_serializers import SimpleRideSerializer

from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    approver = UserSerializer(source="approver.user")
    approvee = UserSerializer(source="approvee.user")
    ride = SimpleRideSerializer()

    class Meta:
        model = Request
        fields = ("id", "approvee", "approver", "ride", "approved", "timestamp")
        read_only_fields = fields

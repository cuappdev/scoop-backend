from person.simple_serializers import SimplePersonSerializer
from rest_framework import serializers
from ride.simple_serializers import SimpleRideSerializer

from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    approver = SimplePersonSerializer()
    approvee = SimplePersonSerializer()
    ride = SimpleRideSerializer()

    class Meta:
        model = Request
        fields = ("id", "approvee", "approver", "ride", "approved")
        read_only_fields = fields

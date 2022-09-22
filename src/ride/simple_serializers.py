from path.serializers import PathSerializer
from rest_framework import serializers

from .models import Ride


class SimpleRideSerializer(serializers.ModelSerializer):
    path = PathSerializer()

    class Meta:
        model = Ride
        fields = (
            "id",
            "departure_datetime",
            "path",
            "type",
        )
        read_only_fields = fields

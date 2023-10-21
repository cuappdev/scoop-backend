from path.serializers import PathSerializer
from person.simple_serializers import SimplePersonSerializer
from rest_framework import serializers

from .models import Ride


class SimpleRideSerializer(serializers.ModelSerializer):
    driver = SimplePersonSerializer()
    path = PathSerializer()

    class Meta:
        model = Ride
        fields = (
            "id",
            "description",
            "departure_datetime",
            "driver",
            "min_travelers",
            "max_travelers",
            "path",
            "ride_type",
        )
        read_only_fields = fields

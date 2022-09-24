from path.serializers import PathSerializer
from person.simple_serializers import SimplePersonSerializer
from rest_framework import serializers
from ride.models import Ride


class RideSerializer(serializers.ModelSerializer):

    creator = SimplePersonSerializer()
    driver = SimplePersonSerializer()
    riders = SimplePersonSerializer(many=True)
    path = PathSerializer()

    class Meta:
        model = Ride
        fields = (
            "id",
            "creator",
            "max_travelers",
            "min_travelers",
            "departure_datetime",
            "description",
            "driver",
            "is_flexible",
            "riders",
            "estimated_cost",
            "path",
            "type",
        )
        read_only_fields = fields

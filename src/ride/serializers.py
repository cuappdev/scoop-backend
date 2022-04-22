from path.serializers import PathSerializer
from person.serializers import UserSerializer
from rest_framework import serializers
from ride.models import Ride


class RideSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="path.id")
    creator = UserSerializer()
    driver = UserSerializer()
    riders = UserSerializer(many=True)
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

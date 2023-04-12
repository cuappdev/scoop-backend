from path.serializers import PathSerializer
from person.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from ride.models import Ride


class RideSerializer(serializers.ModelSerializer):
    creator = SerializerMethodField("get_creator")
    driver = SerializerMethodField("get_driver")
    riders = SerializerMethodField("get_riders")
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

    def get_creator(self, ride):
        return (
            UserSerializer(ride.creator.user).data if ride.creator is not None else None
        )

    def get_driver(self, ride):
        return (
            UserSerializer(ride.driver.user).data if ride.driver is not None else None
        )

    def get_riders(self, ride):
        return [UserSerializer(rider.user).data for rider in ride.riders.all()]

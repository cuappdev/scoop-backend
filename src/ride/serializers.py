from path.serializers import PathSerializer
from person.serializers import UserSerializer
from rest_framework import serializers
from ride.models import Ride


class RideSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField("get_creator")
    max_travelers = serializers.IntegerField(source="ride.max_travelers")
    min_travelers = serializers.IntegerField(source="ride.min_travelers")
    datetime = serializers.DateTimeField(source="ride.datetime")
    description = serializers.CharField(source="ride.description")
    driver = serializers.SerializerMethodField("get_driver")
    is_flexible = serializers.BooleanField(source="ride.is_flexible")
    riders = UserSerializer(source="ride.riders")
    estimated_cost = serializers.FloatField(source="ride.estimated_cost")
    path = serializers.SerializerMethodField("get_path")
    type = serializers.CharField(source="ride.type")

    class Meta:
        model = Ride
        fields = (
            "id",
            "creator",
            "max_travelers",
            "min_travelers",
            "datetime",
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
        creator = UserSerializer(ride.creator).data
        if creator == {}:
            return None
        return creator

    def get_driver(self, ride):
        driver = UserSerializer(ride.driver).data
        if driver == {}:
            return None
        return driver

    def get_path(self, ride):
        path = PathSerializer(ride.path).data
        if path == {}:
            return None
        return path

from django.contrib.auth.models import User
from path.serializers import PathSerializer
from person.serializers import UserSerializer
from rest_framework import serializers
from ride.models import Ride


class RideSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="path.id")
    creator = serializers.SerializerMethodField("get_creator")
    driver = serializers.SerializerMethodField("get_driver")
    riders = serializers.SerializerMethodField("get_riders")
    path = serializers.SerializerMethodField("get_path")

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
        if not ride.creator:
            return None
        if User.objects.filter(id=ride.creator.id).exists():
            return None
        creator = UserSerializer(User.objects.get(id=ride.creator.id)).data
        if creator == {}:
            return None
        return creator

    def get_driver(self, ride):
        if not ride.driver:
            return None
        if User.objects.filter(id=ride.driver.id).exists():
            return None
        driver = UserSerializer(User.objects.get(id=ride.driver.id)).data
        if driver == {}:
            return None
        return driver

    def get_riders(self, ride):
        riders = ride.riders.values_list("id")
        if riders.count() == 0:
            return None
        return UserSerializer(
            User.objects.get(id__in=ride.riders.values_list("id"))
        ).data

    def get_path(self, ride):
        path = PathSerializer(ride.path).data
        if path == {}:
            return None
        return path

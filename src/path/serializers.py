from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from ride.models import Path


class PathSerializer(serializers.ModelSerializer):
    start_coords = SerializerMethodField("get_start_coords")
    end_coords = SerializerMethodField("get_end_coords")

    class Meta:
        model = Path
        fields = (
            "id",
            "start_location_place_id",
            "start_location_name",
            "start_coords",
            "end_location_place_id",
            "end_location_name",
            "end_coords",
        )
        read_only_fields = fields

    def get_start_coords(self, path):
        return (path.start_lat, path.start_lng)

    def get_end_coords(self, path):
        return (path.end_lat, path.end_lng)

from rest_framework import serializers
from ride.models import Path


class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = (
            "id",
            "start_location_place_id",
            "start_location_name",
            "end_location_place_id",
            "end_location_name",
        )
        read_only_fields = fields

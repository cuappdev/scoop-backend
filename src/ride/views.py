import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from rest_framework import generics
from rest_framework import status

from .controllers.create_ride_controller import CreateRideController
from .controllers.search_ride_controller import SearchRideController
from .controllers.update_ride_controller import UpdateRideController
from .models import Ride
from .serializers import RideSerializer


class RidesView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all rides."""
        return success_response(
            self.serializer_class(Ride.objects.all(), many=True).data
        )

    def post(self, request):
        """Create a ride."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateRideController(request, data, self.serializer_class).process()


class RideView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get ride by id."""
        if not Ride.objects.filter(id=id).exists():
            return failure_response("Ride does not exist")
        ride = Ride.objects.get(id=id)
        return success_response(self.serializer_class(ride).data, status.HTTP_200_OK)

    def post(self, request, id):
        """Update ride by id"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateRideController(request, data, self.serializer_class, id).process()

    def delete(self, request, id):
        """Delete ride by id"""
        if not Ride.objects.filter(id=id).exists():
            return failure_response("Ride does not exist")
        ride = Ride.objects.get(id=id)
        ride.delete()
        return success_response("Ride deleted", status.HTTP_200_OK)


class SearchView(generics.GenericAPIView):
    serializer_class = RideSerializer
    lookup_fields = ['depart', 'daysbefore', 'daysafter', 'start', 'end', 'radius']

    def get(self, request, depart, daysbefore, daysafter, start, end, radius):
        """Search for a ride."""
        data = {
            "departure_datetime": depart,
            "days_before": daysbefore,
            "days_after": daysafter,
            "start_location_place_id": start,
            "end_location_place_id": end,
            "radius": radius
        }
        return SearchRideController(data, self.serializer_class).process()

import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from rest_framework import generics
from rest_framework import status
from django.utils import timezone

from .controllers.create_ride_controller import CreateRideController
from .controllers.search_ride_controller import SearchRideController
from .controllers.update_ride_controller import UpdateRideController
from .models import Ride
from .serializers import RideSerializer


class RidesView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all rides in the future."""
        return success_response(
            self.serializer_class(Ride.objects.filter(departure_datetime__gt=timezone.now()), many=True).data
        )

    def post(self, request):
        """Create a ride."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateRideController(request, data, self.serializer_class).process()
    

class RidesArchiveView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all rides, including already-departed rides."""
        return success_response(
            self.serializer_class(Ride.objects.all(), many=True).data
        )


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
    # test


class SearchView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request):
        """Search for a ride."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data

        return SearchRideController(data, request, self.serializer_class).process()

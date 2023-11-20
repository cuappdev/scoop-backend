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
from .controllers.recent_rides_controller import RecentRidesController
from ride.utils import MultipleFieldLookupMixin
from .models import Ride
from .serializers import RideSerializer
from .simple_serializers import SimpleRideSerializer


class RidesView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all rides in the future from unblocked users."""
        return success_response(
            self.serializer_class(Ride.objects.filter(departure_datetime__gt=timezone.now(), archived=False).exclude(creator__in=blocked_users), many=True).data
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
        if ride.archived:
            return failure_response("Ride does not exist")
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
        ride.archived = True
        ride.save()
        return success_response("Ride deleted", status.HTTP_200_OK)


class SearchView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    lookup_fields = ['time', 'start', 'end', 'radius']

    def get(self, request, time, start, end, radius):
        """Search for a ride."""
        data = {
            "departure_datetime": time,
            "start_location_place_id": start,
            "end_location_place_id": end,
            "radius": radius
        }
        return SearchRideController(data, self.serializer_class).process()

      
class RecentView(generics.GenericAPIView):
    serializer_class = SimpleRideSerializer

    def get(self, request):
        """Get recent rides."""
        return RecentRidesController(self.serializer_class).process()

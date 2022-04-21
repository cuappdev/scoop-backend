import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from rest_framework import generics
from rest_framework import status

from .controllers.create_ride_controller import CreateRideController
from .models import Ride
from .serializers import RideSerializer


class AllRidesView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all rides."""
        rides = [self.serializer_class(ride).data for ride in Ride.objects.all()]
        return success_response(rides)


class RideView(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get ride by id."""
        id = request.query_params.get("id", None)
        if not id:
            return failure_response("Missing id")
        if not Ride.objects.filter(path_id=int(id)).exists():
            return failure_response("Ride does not exist")
        ride = Ride.objects.get(path_id=int(id))
        return success_response(self.serializer_class(ride).data, status.HTTP_200_OK)

    def post(self, request):
        """Create a ride."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateRideController(request, data, self.serializer_class).process()
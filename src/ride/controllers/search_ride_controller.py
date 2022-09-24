from api.utils import failure_response
from api.utils import success_response
from api.utils import update
from django.core.exceptions import ObjectDoesNotExist
from person.models import Person

from ..models import Ride
from ..models import Path

class SearchRideController:
    def __init__(self, data, request, serializer): 
        self._request = request
        self._data = data
        self._serializer = serializer

    def process(self):
        departure_datetime = self._data.get("departure_datetime")
        start_location_name = self._data.get("start_location_name")
        end_location_name = self._data.get("end_location_name")
        if not (Path.objects.filter(start_location_name = start_location_name, end_location_name = end_location_name)).exists():
            return failure_response("Path does not exist.")
        
        path = Path.objects.get(start_location_name = start_location_name, end_location_name = end_location_name)

        if not (Ride.objects.filter(path = path)):
            return failure_response("Ride with that path does not exist")
        all_rides = Ride.objects.filter(path = path)

        return success_response(self._serializer(all_rides, many=True).data)

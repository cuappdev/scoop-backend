from api.utils import failure_response
from api.utils import success_response
from api.utils import update
from django.core.exceptions import ObjectDoesNotExist
from person.models import Person

from ..models import Ride


class UpdateRideController:
    def __init__(self, request, data, serializer, id):
        self._request = request
        self._data = data
        self._serializer = serializer
        self._id = id

    def process(self):
        if not Ride.objects.filter(path_id=int(self._id)).exists():
            return failure_response("Ride does not exist")
        ride = Ride.objects.get(path_id=self._id)
        path = ride.path

        # Extract attributes
        max_travelers = self._data.get("max_travelers")
        min_travelers = self._data.get("min_travelers")
        description = self._data.get("description", "")
        departure_datetime = self._data.get("departure_datetime")
        driver_id = self._data.get("driver")
        rider_ids = self._data.get("riders")
        is_flexible = self._data.get("is_flexible")
        start_location_place_id = self._data.get("start_location_place_id")
        start_location_name = self._data.get("start_location_name")
        end_location_place_id = self._data.get("end_location_place_id")
        end_location_name = self._data.get("end_location_name")
        type = self._data.get("type")

        # Modify new values
        if driver_id is not None and Person.objects.filter(id=driver_id).exists():
            driver = Person.objects.get(id=driver_id)
            update(ride, "driver", driver)
        elif ride.driver is not None:
            # if driver removes themself from ride
            ride.driver = None

        if rider_ids is not None:
            try:
                ride.riders.set([Person.objects.get(id=rider) for rider in rider_ids])
            except ObjectDoesNotExist:
                return failure_response("Invalid rider passed in")

        update(ride, "max_travelers", max_travelers)
        update(ride, "min_travelers", min_travelers)
        update(ride, "description", description)
        update(ride, "departure_datetime", departure_datetime)
        update(ride, "is_flexible", is_flexible)
        update(ride, "type", type)

        update(path, "start_location_place_id", start_location_place_id)
        update(path, "start_location_name", start_location_name)
        update(path, "end_location_place_id", end_location_place_id)
        update(path, "end_location_name", end_location_name)

        # Save new changes
        ride.save()
        path.save()
        ride = Ride.objects.get(path_id=ride.path_id)
        return success_response(self._serializer(ride).data)

from api.utils import success_response
from api.utils import update
from api.utils import update_many_to_many_set
from person.models import Person

from ..models import Ride


class UpdateRideController:
    def __init__(self, request, data, serializer, id):
        self._request = request
        self._data = data
        self._serializer = serializer
        self._ride = Ride.objects.get(path_id=id)
        self._path = self._ride.path

    def process(self):
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

        if driver_id is not None and Person.objects.filter(id="driver_id").exists():
            driver = Person.objects.get(id="driver_id")
            update(self._ride, "driver", driver)
        elif self._ride.driver is not None:
            # if driver removes themself from ride
            self._ride.driver = None

        optional_error = update_many_to_many_set(Person, self._ride.riders, rider_ids)
        if optional_error is not None:
            return optional_error

        update(self._ride, "max_travelers", max_travelers)
        update(self._ride, "min_travelers", min_travelers)
        update(self._ride, "description", description)
        update(self._ride, "departure_datetime", departure_datetime)
        update(self._ride, "is_flexible", is_flexible)
        update(self._ride, "type", type)

        update(self._path, "start_location_place_id", start_location_place_id)
        update(self._path, "start_location_name", start_location_name)
        update(self._path, "end_location_place_id", end_location_place_id)
        update(self._path, "end_location_name", end_location_name)

        self._ride.save()
        self._path.save()

        self._ride = Ride.objects.get(path_id=self._ride.path_id)
        return success_response(self._serializer(self._ride).data)

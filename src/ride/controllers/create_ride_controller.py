from os import environ

from api.utils import failure_response
from api.utils import success_response
from path.models import Path
from person.models import Person
import requests
from rest_framework import status

from ..models import Ride


class CreateRideController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer

    def process(self):
        creator = self._data.get("creator")
        driver = self._data.get("driver")
        max_travelers = self._data.get("max_travelers")
        min_travelers = self._data.get("min_travelers")
        description = self._data.get("description", "")
        departure_datetime = self._data.get("departure_datetime")
        is_flexible = self._data.get("is_flexible")
        start_location_place_id = self._data.get("start_location_place_id")
        start_location_name = self._data.get("start_location_name")
        end_location_place_id = self._data.get("end_location_place_id")
        end_location_name = self._data.get("end_location_name")
        type = self._data.get("type")

        # Verify all required information is provided
        if (
            start_location_place_id is None
            or start_location_name is None
            or end_location_name is None
            or end_location_place_id is None
        ):
            return failure_response("Missing path information", 400)

        if (
            is_flexible is None
            or departure_datetime is None
            or type is None
            or min_travelers is None
            or max_travelers is None
            or creator is None
        ):
            return failure_response("Missing ride information", 400)

        driver_person = Person.objects.filter(id=int(driver)).exists()
        if not driver_person:
            return failure_response("Driver does not exist")
        driver_person = Person.objects.get(id=driver)

        creator_person = Person.objects.filter(id=int(creator)).exists()
        if not creator_person:
            return failure_response("Creator does not exist")
        creator_person = Person.objects.get(id=creator)

        # Create new path or retrieve existing path
        path_exists = Path.objects.filter(
            start_location_place_id=start_location_place_id,
            end_location_place_id=end_location_place_id,
        ).exists()
        if not path_exists:
            # Get latitude and longitude of start and end location
            params = {
                "place_id": start_location_place_id,
                "key": environ.get("GOOGLE_API_KEY"),
            }
            response = requests.get(
                "https://maps.googleapis.com/maps/api/place/details/json", params=params
            )
            if response.status_code == 200:
                start_coords = (
                    response.json()["result"]["geometry"]["location"]["lat"],
                    response.json()["result"]["geometry"]["location"]["lng"],
                )
            else:
                return failure_response("Invalid Google Places ID")

            params["place_id"] = end_location_place_id
            response = requests.get(
                "https://maps.googleapis.com/maps/api/place/details/json", params=params
            )
            if response.status_code == 200:
                end_coords = (
                    response.json()["result"]["geometry"]["location"]["lat"],
                    response.json()["result"]["geometry"]["location"]["lng"],
                )
            else:
                return failure_response("Invalid Google Places ID")

            path = Path.objects.create(
                start_location_place_id=start_location_place_id,
                start_location_name=start_location_name,
                start_lat=start_coords[0],
                start_lng=start_coords[1],
                end_location_place_id=end_location_place_id,
                end_location_name=end_location_name,
                end_lat=end_coords[0],
                end_lng=end_coords[1],
            )
            path.save()
        else:
            path = Path.objects.get(
                start_location_place_id=start_location_place_id,
                end_location_place_id=end_location_place_id,
            )

        # Create new ride
        ride = Ride.objects.create(
            driver=driver_person,
            creator=creator_person,
            max_travelers=max_travelers,
            description=description,
            departure_datetime=departure_datetime,
            is_flexible=is_flexible,
            type=type,
            path=path,
        )
        ride.save()

        return success_response(self._serializer(ride).data, status.HTTP_201_CREATED)

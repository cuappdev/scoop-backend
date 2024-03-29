import datetime
from os import environ

from api.utils import failure_response
from api.utils import success_response
import geopy.distance
import requests
from rideshare.settings import TIME_ZONE
import zoneinfo

from ..models import Path
from ..models import Ride


class SearchRideController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        departure_datetime = self._data.get("departure_datetime")
        start_location_place_id = self._data.get("start_location_place_id")
        end_location_place_id = self._data.get("end_location_place_id")
        radius = self._data.get("radius")

        if departure_datetime:
            tz = zoneinfo.ZoneInfo(TIME_ZONE)
            departure_datetime_object = datetime.datetime.fromisoformat(
                departure_datetime
            ).astimezone(tz)

            departure_last_week = departure_datetime_object - datetime.timedelta(days=7)
            departure_next_week = departure_datetime_object + datetime.timedelta(days=7)

        # Only searching by departure time
        if departure_datetime and not start_location_place_id and not end_location_place_id and not radius:
            all_rides = Ride.objects.filter(
                departure_datetime__gte=departure_last_week,
                departure_datetime__lte=departure_next_week,
                departure_datetime__gt=timezone.now()
            )

            # Sort results based on time proximity
            all_rides = sorted(
                all_rides,
                key=lambda ride: (
                    abs(departure_datetime_object - ride.departure_datetime),
                ),
            )

        else:
            # Get latitude and longitude of start and end locations
            if start_location_place_id:
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

            if end_location_place_id:
                params = {
                    "place_id": end_location_place_id,
                    "key": environ.get("GOOGLE_API_KEY"),
                }
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

            paths = []

            # Only searching by start location
            if start_location_place_id and radius and not end_location_place_id and not departure_datetime:
                for path in Path.objects.all():
                    path_start_coords = (path.start_lat, path.start_lng)
                    if (
                        geopy.distance.geodesic(path_start_coords, start_coords).miles < radius
                    ):
                        paths.append(path)
                
                all_rides = Ride.objects.filter(
                    path__in=paths,
                    departure_datetime__gt=timezone.now()
                )

                # Sort results based on location
                all_rides = sorted(
                    all_rides,
                    key=lambda ride: (
                        geopy.distance.geodesic(
                            (ride.path.start_lat, ride.path.start_lng), start_coords
                        ).miles
                    ),
                )
            
            # Only searching by end location
            elif end_location_place_id and radius and not start_location_place_id and not departure_datetime:
                for path in Path.objects.all():
                    path_end_coords = (path.end_lat, path.end_lng)
                    if (
                        geopy.distance.geodesic(path_end_coords, end_coords).miles < radius
                    ):
                        paths.append(path)
                
                all_rides = Ride.objects.filter(
                    path__in=paths,
                    departure_datetime__gt=timezone.now()
                )

                # Sort results based on location
                all_rides = sorted(
                    all_rides,
                    key=lambda ride: (geopy.distance.geodesic(
                            (ride.path.end_lat, ride.path.end_lng), end_coords
                        ).miles
                    ),
                )
            
            # Searching by departure time and start location
            elif departure_datetime and start_location_place_id and radius and not end_location_place_id:
                for path in Path.objects.all():
                    path_start_coords = (path.start_lat, path.start_lng)
                    if (
                        geopy.distance.geodesic(path_start_coords, start_coords).miles < radius
                    ):
                        paths.append(path)

                all_rides = Ride.objects.filter(
                    path__in=paths,
                    departure_datetime__gte=departure_last_week,
                    departure_datetime__lte=departure_next_week,
                    departure_datetime__gt=timezone.now()
                )

                # Sort results based on location and time proximity
                all_rides = sorted(
                    all_rides,
                    key=lambda ride: (
                        geopy.distance.geodesic(
                            (ride.path.start_lat, ride.path.start_lng), start_coords
                        ).miles,
                        abs(departure_datetime_object - ride.departure_datetime),
                    ),
                )

            # Searching by departure time and end location
            elif departure_datetime and end_location_place_id and radius and not start_location_place_id:
                for path in Path.objects.all():
                    path_end_coords = (path.end_lat, path.end_lng)
                    if (
                        geopy.distance.geodesic(path_end_coords, end_coords).miles < radius
                    ):
                        paths.append(path)

                all_rides = Ride.objects.filter(
                    path__in=paths,
                    departure_datetime__gte=departure_last_week,
                    departure_datetime__lte=departure_next_week,
                    departure_datetime__gt=timezone.now()
                )

                # Sort results based on location and time proximity
                all_rides = sorted(
                    all_rides,
                    key=lambda ride: (
                        geopy.distance.geodesic(
                            (ride.path.end_lat, ride.path.end_lng), end_coords
                        ).miles,
                        abs(departure_datetime_object - ride.departure_datetime),
                    ),
                )

            # Searching by start and end location
            elif start_location_place_id and end_location_place_id and radius and not departure_datetime:
                for path in Path.objects.all():
                    path_start_coords = (path.start_lat, path.start_lng)
                    path_end_coords = (path.end_lat, path.end_lng)
                    if (
                        geopy.distance.geodesic(path_start_coords, start_coords).miles < radius
                        and geopy.distance.geodesic(path_end_coords, end_coords).miles < radius
                    ):
                        paths.append(path)

                all_rides = Ride.objects.filter(
                    path__in=paths,
                    departure_datetime__gt=timezone.now()
                )

                # Sort results based on location
                all_rides = sorted(
                    all_rides,
                    key=lambda ride: (
                        geopy.distance.geodesic(
                            (ride.path.start_lat, ride.path.start_lng), start_coords
                        ).miles
                        + geopy.distance.geodesic(
                            (ride.path.end_lat, ride.path.end_lng), end_coords
                        ).miles,
                    ),
                )

            # Searching by all parameters
            elif departure_datetime and start_location_place_id and end_location_place_id and radius:
                for path in Path.objects.all():
                    path_start_coords = (path.start_lat, path.start_lng)
                    path_end_coords = (path.end_lat, path.end_lng)
                    if (
                        geopy.distance.geodesic(path_start_coords, start_coords).miles < radius
                        and geopy.distance.geodesic(path_end_coords, end_coords).miles < radius
                    ):
                        paths.append(path)

                all_rides = Ride.objects.filter(
                    path__in=paths,
                    departure_datetime__gte=departure_last_week,
                    departure_datetime__lte=departure_next_week,
                    departure_datetime__gt=timezone.now()
                )

                # Sort results based on location and time proximity
                all_rides = sorted(
                    all_rides,
                    key=lambda ride: (
                        geopy.distance.geodesic(
                            (ride.path.start_lat, ride.path.start_lng), start_coords
                        ).miles
                        + geopy.distance.geodesic(
                            (ride.path.end_lat, ride.path.end_lng), end_coords
                        ).miles,
                        abs(departure_datetime_object - ride.departure_datetime),
                    ),
                )

        return success_response(self._serializer(all_rides, many=True).data)
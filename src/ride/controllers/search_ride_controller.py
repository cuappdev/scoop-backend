import datetime

from api.utils import success_response

from ..models import Path
from ..models import Ride


class SearchRideController:
    def __init__(self, data, request, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer

    def process(self):
        departure_datetime = self._data.get("departure_datetime")
        start_location_name = self._data.get("start_location_name")
        end_location_name = self._data.get("end_location_name")
        if not (
            Path.objects.filter(
                start_location_name=start_location_name,
                end_location_name=end_location_name,
            )
        ).exists():
            return success_response()

        departure_datetime_object = datetime.datetime.fromisoformat(departure_datetime)

        departure_yesterday = departure_datetime_object - datetime.timedelta(days=1)
        departure_tomorrow = departure_datetime_object + datetime.timedelta(days=1)

        path = Path.objects.get(
            start_location_name__iexact=start_location_name,
            end_location_name__iexact=end_location_name,
        )

        all_rides = Ride.objects.filter(
            path=path,
            departure_datetime__gte=departure_yesterday,
            departure_datetime__lte=departure_tomorrow,
        )

        return success_response(self._serializer(all_rides, many=True).data)

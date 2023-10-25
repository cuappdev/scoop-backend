import datetime

from api.utils import success_response
from rideshare.settings import TIME_ZONE
import zoneinfo

from ..models import Ride


class RecentRidesController:
    def __init__(self, serializer):
        self._serializer = serializer

    def process(self):
        tz = zoneinfo.ZoneInfo(TIME_ZONE)

        departure_start = datetime.datetime.now(tz)
        departure_end = datetime.datetime.now(tz) + datetime.timedelta(days=7)

        recent_rides = Ride.objects.filter(
            departure_datetime__gte=departure_start,
            departure_datetime__lte=departure_end,
        )

        # Sort results from most recent to least
        recent_rides = sorted(
            recent_rides,
            key=lambda ride: (
                abs(departure_start - ride.departure_datetime),
            ),
        )

        return success_response(self._serializer(recent_rides, many=True).data)

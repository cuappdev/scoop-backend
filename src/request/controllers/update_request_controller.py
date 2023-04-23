from api.utils import failure_response
from api.utils import success_response
from api.utils import update
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from person.models import Person
from ride.models import Ride

from ..models import Request


class UpdateRequestController:
    def __init__(self, request, data, serializer, id):
        self._request = request
        self._data = data
        self._serializer = serializer
        self._id = id

    def process(self):
        requests = Request.objects.filter(id=int(self._id))
        if len(requests) != 1:
            return failure_response("Request does not exist")
        request = requests.first()

        # Extract attributes
        approved = self._data.get("approved")

        # Modify new values
        update(request, "approved", approved)

        # If request is approved, add rider to ride
        if approved:
            ride = Ride.objects.get(id=request.ride.id)
            rider_ids = [request.approvee.id]
            if len(ride.riders.all()) > 0:
                past_riders = [rider.id for rider in ride.riders.all()]
                rider_ids += past_riders
            try:
                ride.riders.set([Person.objects.get(id=rider) for rider in rider_ids])
            except ObjectDoesNotExist:
                return failure_response("Invalid rider passed in")
            ride.save()

        # If approved is not None or ride's departure deadline has passed, delete request
        if approved is not None or ride.departure_datetime < timezone.now():
            Request.objects.filter(id=self._id).delete()

        # Save new changes
        request.save()
        request = Request.objects.get(id=int(self._id))
        return success_response(self._serializer(request).data)

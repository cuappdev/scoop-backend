from api.utils import failure_response
from api.utils import success_response
from person.models import Person
from rest_framework import status
from ride.models import Ride

from ..models import Request


class CreateRequestController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer

    def process(self):
        approvee_id = self._data.get("approvee_id")
        ride_id = self._data.get("ride_id")

        # Verify all required information is provided
        if approvee_id is None or ride_id is None:
            return failure_response("Missing request information", 400)

        approvee_exists = Person.objects.filter(id=int(approvee_id)).exists()
        if not approvee_exists:
            return failure_response("Approvee does not exist")
        approvee = Person.objects.get(id=approvee_id)

        ride_exists = Ride.objects.filter(id=int(ride_id)).exists()
        if not ride_exists:
            return failure_response("Ride does not exist")
        ride = Ride.objects.get(id=ride_id)
        approver = ride.creator

        # Create request and return new request with given fields
        request = Request.objects.create(
            approvee=approvee,
            approver=approver,
            ride=ride,
        )
        request.save()

        return success_response(self._serializer(request).data, status.HTTP_201_CREATED)

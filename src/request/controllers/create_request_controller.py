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
        elif type(approvee_id) != int or type(ride_id) != int:
            return failure_response("Approvee ID and/or ride ID is not int")

        users = Person.objects.filter(id=approvee_id)
        if len(users) != 1:
            return failure_response("Approvee does not exist")
        approvee = users[0]

        rides = Ride.objects.filter(id=ride_id)
        if len(rides) != 1:
            return failure_response("Ride does not exist")
        ride = rides[0]
        approver = ride.creator

        request_exists = Request.objects.filter(
            approvee=approvee, approver=approver, ride=ride
        ).exists()
        if request_exists:
            return failure_response("Request already exists for this ride")

        # Create request and return new request with given fields
        request = Request.objects.create(
            approvee=approvee,
            approver=approver,
            ride=ride,
        )
        request.save()

        return success_response(self._serializer(request).data, status.HTTP_201_CREATED)

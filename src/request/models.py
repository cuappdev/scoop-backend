from django.db import models
from person.models import Person
from ride.models import Ride


class Request(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    approvee = models.ForeignKey(
        Person, on_delete=models.CASCADE, default=None, related_name="approvee"
    )
    approver = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        default=None,
        related_name="approver",
        null=True,
    )
    approved = models.BooleanField(default=None, null=True)

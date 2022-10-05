from django.db import models
from path.models import Path
from person.models import Person


class Ride(models.Model):
    RIDE_TYPES = [("rideshare", "Rideshare"), ("studentdriver", "Student Driver")]

    creator = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True, related_name="creator"
    )
    max_travelers = models.IntegerField(default=1)  # max number of travelers
    min_travelers = models.IntegerField(default=1)  # min number of travelers
    departure_datetime = models.DateTimeField()  # date and time of travel
    description = models.TextField(default=None, null=True)
    driver = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True, related_name="driver"
    )
    is_flexible = models.BooleanField(default=False)
    riders = models.ManyToManyField(Person)
    estimated_cost = models.FloatField(default=None, null=True)
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=RIDE_TYPES)

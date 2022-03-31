from django.db import models
from path.models import Path
from person.models import Person


class Ride(models.Model):
    creator = models.ForeignKey(Person, on_delete=models.SET_NULL)
    num_travelers = models.IntegerField()
    driver = models.ManyToManyField(
        Person, default=None, blank=True, related_name="driver"
    )
    riders = models.TextField(null=True)
    estimated_cost = models.FloatField(null=True)
    path = models.OneToOneField(Path, on_delete=models.CASCADE, primary_key=True)
    RIDE_TYPES = ["Rideshare", "Student Driver"]
    type = models.CharField(max_length=20, choices=RIDE_TYPES)

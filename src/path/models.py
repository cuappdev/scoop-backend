from django.db import models


class Path(models.Model):
    start_location_id = models.TextField()
    start_location_name = models.TextField()
    end_location = models.TextField()
    end_location_name = models.TextField()
    time = models.DateTimeField()
    is_flexible = models.BooleanField(default=False)
    description = models.TextField(default=None, null=True)
    estimated_cost = models.FloatField(default=None, null=True)

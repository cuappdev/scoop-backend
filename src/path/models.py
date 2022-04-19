from django.db import models


class Path(models.Model):
    start_location_id = models.TextField()
    start_location_name = models.TextField()
    end_location = models.TextField()
    end_location_name = models.TextField()

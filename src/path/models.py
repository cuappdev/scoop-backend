from django.db import models


class Path(models.Model):
    start_location_place_id = models.TextField()  # start location ID from Google Places
    start_location_name = models.TextField()
    end_location_place_id = models.TextField()  # end location ID from Google Places
    end_location_name = models.TextField()

from django.db import models


class Path(models.Model):
    start_location_place_id = models.TextField()  # start location ID from Google Places
    start_location_name = models.TextField()
    start_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    start_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    end_location_place_id = models.TextField()  # end location ID from Google Places
    end_location_name = models.TextField()
    end_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    end_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True)

import geopy.distance
from api.utils import success_response

class PriceController:
    # Average car has 25 miles/gallon
    MPG = 25
    # October 2023 verage gas price is $3.925 (regular gas)
    GAS_PRICE = 3.925

    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        path = self._data.get("path")

        path_start_coords = (path.start_lat, path.start_lng)
        path_end_coords = (path.end_lat, path.end_lng)

        expected_price = geopy.distance.geodesic(path_start_coords, path_end_coords).miles * (1/PriceController.MPG) * (PriceController.GAS_PRICE)

        return success_response({"expected price": expected_price})
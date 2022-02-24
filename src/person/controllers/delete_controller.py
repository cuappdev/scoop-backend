from app.utils import success_response
from rest_framework import status


class DeletePersonController:
    def __init__(self, user, data, serializer):
        self._data = data
        self._serializer = serializer
        self._user = user
        self._person = self._user.person

    def process(self):
        self._user.delete()
        self._person.delete()
        return success_response(status=status.HTTP_200_OK)

from random import randint

from app.utils import success_response
from django.contrib.auth.models import User
from person.models import Person
from rest_framework import status
from rest_framework.authtoken.models import Token


class DeveloperController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer

    def create_person(self, person_data):
        """Creates new Person object from person_data"""
        person = Person(**person_data)
        person.save()
        return person

    def create_user(self, user_data):
        """Creates new user (Django auth) from user_data"""
        return User.objects._create_user(**user_data)

    def process(self):
        status_code = status.HTTP_200_OK
        user_id = self._data.get("user_id")
        if user_id is None:
            user_data = {
                "username": self._data.get("username"),
                "email": self._data.get("username"),
                "password": self._data.get("password"),
                "first_name": self._data.get("first_name"),
                "last_name": self._data.get("last_name"),
            }
            user = self.create_user(user_data)
            person_data = {"user": user, "netid": "test" + str(randint(0, 100))}
            self.create_person(person_data)
            status_code = status.HTTP_201_CREATED
        else:
            user = User.objects.filter(id=int(user_id)).first()
        access_token, _ = Token.objects.get_or_create(user=user)
        return success_response(
            self._serializer(user, context={"access_token": access_token.key}).data,
            status_code,
        )

import api.settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from person.models import Person
from rest_framework import status
from rest_framework.authtoken.models import Token


class AuthenticateController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer

    def authenticate(self, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            return None, status.HTTP_403_FORBIDDEN
        login(self._request, user)
        return user, status.HTTP_200_OK

    def create_access_token(self, user):
        """Creates or retrieves current access token for user. If expired, then create new access token."""
        token, _ = Token.objects.get_or_create(user=user)
        elapsed_seconds = (timezone.now() - token.created).total_seconds()
        if api_settings.ACCESS_TOKEN_AGE <= elapsed_seconds:
            token.delete()
            token = Token.objects.create(user=user)
        return token.key

    def create_user(self, user_data):
        """Creates new user (Django auth) from `user_data`"""
        return User.objects.create_user(**user_data)

    def create_person(self, person_data):
        """Creates new Person object from `person_data`"""
        person = Person(**person_data)
        person.save()
        return person

    def create_token_info(self, token_info):
        """Create token info for app based on Google `token_info`"""
        username = token_info.get("email")
        google_user_id = token_info.get("sub")
        password = api_settings.AUTH_PASSWORD_SALT + google_user_id
        first_name = token_info.get("given_name")
        last_name = token_info.get("family_name")
        netid = token_info.get("email").split("@")[0]
        return netid, username, password, first_name, last_name

    def get_token_info(self, token):
        """Returns token information if `token` is valid."""
        if not api_settings.GOOGLE_DEBUG:
            try:
                return id_token.verify_oauth2_token(token, requests.Request())
            except ValueError:
                return None
        return self._data

    def login(self, token_info):
        """Logs user in given `token_info`. If user does not exist, registers new one."""
        netid, username, password, _, _ = self.create_token_info(token_info)
        person_exists = Person.objects.filter(netid=netid)
        if not person_exists:
            self.register(token_info)
        user, auth_status = self.authenticate(username, password)
        return (
            user,
            status.HTTP_201_CREATED if not person_exists else auth_status,
        )

    def process(self):
        """Returns the current access token or a new one if expired. If the user isn't authenticated yet,
        logs existing user in or registers a new one."""
        user = self._request.user
        status_code = status.HTTP_200_OK
        if self._data.get("username") and self._data.get("password"):
            user, status_code = self.authenticate(
                self._data.get("username"), self._data.get("password")
            )
            if user is None:
                return failure_response("Bad credentials provided.", status=status_code)
        elif not user.is_authenticated:
            token = self._data.get("id_token")
            token_info = self.get_token_info(token)
            if token_info is None:
                return failure_response(
                    "ID Token is not valid.", status.HTTP_401_UNAUTHORIZED
                )
            user, status_code = self.login(token_info)
            if user is None:
                return failure_response("ID Token is not valid.", status=status_code)
        access_token = self.create_access_token(user)
        return success_response(
            self._serializer(user, context={"access_token": access_token}).data,
            status=status_code,
        )

    def register(self, token_info):
        """Registers new account given `token_info`"""
        (netid, username, password, first_name, last_name) = self.create_token_info(
            token_info
        )
        user_data = {
            "username": username,
            "email": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }
        user = self.create_user(user_data)
        person_data = {"user": user, "netid": netid}
        self.create_person(person_data)

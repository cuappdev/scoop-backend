import json

from app import settings as api_settings
from app.utils import success_response
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status

from .controllers.authenticate_controller import AuthenticateController
from .controllers.delete_controller import DeletePersonController
from .controllers.developer_controller import DeveloperController
from .controllers.update_controller import UpdatePersonController
from .serializer import AuthenticateSerializer
from .serializer import UserSerializer


class AuthenticateView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request):
        """Authenticate the current user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return AuthenticateController(request, data, self.serializer_class).process()


class MeView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get current authenticated user."""
        return success_response(
            self.serializer_class(request.user).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Update current authenticated user"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdatePersonController(
            request.user, data, self.serializer_class
        ).process()

    def delete(self, request):
        """Delete current authenticated user"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return DeletePersonController(
            request.user, data, self.serializer_class
        ).process()


class DeveloperView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer
    permission_classes = api_settings.ADMIN_PERMISSIONS

    def get(self, request):
        """Get all users"""
        people = User.objects.all()
        result = []
        for person in people:
            result.append(UserSerializer(person).data)
        return success_response(result, status.HTTP_200_OK)

    def post(self, request):
        """Create test user or return access token for test user if user_id is provided"""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return DeveloperController(request, data, self.serializer_class).process()

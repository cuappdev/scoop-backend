import json

from api import settings as api_settings
from api.utils import success_response
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status

from .controllers.authenticate_controller import AuthenticateController
from .controllers.developer_controller import DeveloperController
from .controllers.update_controller import UpdatePersonController
from .controllers.block_controller import BlockController, UnblockController
from .serializers import AuthenticateSerializer
from .serializers import UserSerializer


class AuthenticateView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer
    permission_classes = api_settings.UNPROTECTED

    def post(self, request):
        """Authenticate the current user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return AuthenticateController(request, data, self.serializer_class).process()


class BlockView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get blocked users for current authenticated user."""
        return success_response(
            self.serializer_class(map(lambda p: p.user, request.user.person.blocked_users.all()), many=True).data,
            status.HTTP_200_OK,
        )

    def post(self, request):
        """Block a user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return BlockController(
            request.user, data, self.serializer_class
        ).process()


class UnblockView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request):
        """Unblock a user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UnblockController(
            request.user, data, self.serializer_class
        ).process()


class MeView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get current authenticated user."""
        return success_response(
            self.serializer_class(request.user).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Update current authenticated user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdatePersonController(
            request.user, data, self.serializer_class
        ).process()

    def delete(self, request):
        """Delete current authenticated user."""
        request.user.delete()
        return success_response("User deleted", status.HTTP_200_OK)


class DeveloperView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer
    permission_classes = api_settings.ADMIN_PERMISSIONS

    def get(self, request):
        """Get all users."""
        users = [UserSerializer(user).data for user in User.objects.all()]
        return success_response(users)

    def post(self, request):
        """Create test user or return access token for test user if `id` is provided."""
        try:
            data = json.loads(request.body)
            id = request.query_params.get("id", None)
        except json.JSONDecodeError:
            data = request.data
        return DeveloperController(request, data, self.serializer_class, id).process()

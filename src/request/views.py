import json

from api import settings as api_settings
from rest_framework import generics

from .controllers.create_request_controller import CreateRequestController
from .controllers.get_user_requests_controller import GetUserRequestsController
from .controllers.update_request_controller import UpdateRequestController
from .serializers import RequestSerializer


class RequestsView(generics.GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request):
        """Create a request."""
        data = json.loads(request.body)
        return CreateRequestController(request, data, self.serializer_class).process()

    def get(self, request):
        """Get all of a user's active requests."""
        user = request.user.person
        return GetUserRequestsController(request, user, self.serializer_class).process()


class RequestView(generics.GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request, id):
        """Update a request."""
        data = json.loads(request.body)
        return UpdateRequestController(
            request, data, self.serializer_class, id
        ).process()

import json

from api import settings as api_settings
from api.utils import success_response
from rest_framework import generics

from .controllers.create_request_controller import CreateRequestController
from .models import Request
from .serializers import RequestSerializer


class RequestsView(generics.GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request):
        """Create a request."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateRequestController(request, data, self.serializer_class).process()

    def get(self, request):
        """Get all of a user's active requests."""
        user = request.user.person
        awaiting_approval = Request.objects.filter(
            approver=user, approved=None
        ).order_by("timestamp")
        pending_requests = Request.objects.filter(
            approvee=user, approved=None
        ).order_by("timestamp")
        res = {
            "To Approve": self.serializer_class(awaiting_approval, many=True).data,
            "Waiting for Approval": self.serializer_class(
                pending_requests, many=True
            ).data,
        }
        return success_response(res)


class RequestView(generics.GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

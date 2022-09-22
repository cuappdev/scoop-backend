import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from rest_framework import generics
from rest_framework import status

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


class RequestView(generics.GenericAPIView):
    serializer_class = RequestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get request by id."""
        if not Request.objects.filter(id=int(id)).exists():
            return failure_response("Request does not exist")
        req = Request.objects.get(id=int(id))
        return success_response(self.serializer_class(req).data, status.HTTP_200_OK)

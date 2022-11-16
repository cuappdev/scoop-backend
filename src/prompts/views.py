import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from prompts.models import Prompt
from rest_framework import generics
from rest_framework import status

from .controllers.create_prompt_controller import CreatePromptController
from .serializers import PromptSerializer


class PromptsView(generics.GenericAPIView):
    serializer_class = PromptSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all prompts."""
        prompts = Prompt.objects.all()
        return success_response(
            self.serializer_class(prompts, many=True).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Create a prompt."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreatePromptController(data, self.serializer_class).process()


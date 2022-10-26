import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from prompt.models import Prompt
from rest_framework import generics
from rest_framework import status

from .controllers.create_prompt_controller import CreatePromptController
from .controllers.update_prompt_controller import UpdatePromptController
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


class PromptView(generics.GenericAPIView):
    serializer_class = PromptSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get prompt by id."""
        prompt = Prompt.objects.filter(id=id)
        if not prompt:
            return failure_response("Prompt does not exist", status.HTTP_404_NOT_FOUND)
        return success_response(
            self.serializer_class(prompt[0]).data, status.HTTP_200_OK
        )

    def post(self, request, id):
        """Update prompt by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdatePromptController(id, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete prompt by id."""
        prompt = Prompt.objects.filter(id=id)
        if not prompt:
            return failure_response("Prompt does not exist", status.HTTP_404_NOT_FOUND)
        prompt[0].delete()
        return success_response(
            self.serializer_class(prompt[0]).data, status.HTTP_200_OK
        )
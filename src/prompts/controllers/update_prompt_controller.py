from api.utils import failure_response
from api.utils import update
from api.utils import success_response
from prompts.models import Prompt
from rest_framework import status 

class UpdatePromptController:
    def __init__(self, id, data, serializer):
        self._id = id
        self._data = data
        self._serializer = serializer

    def process(self):
        # Get the model
        prompt = Prompt.objects.filter(id=self._id)
        if not prompt:
            return failure_response("Prompt does not exist", status.HTTP_404_NOT_FOUND)
        prompt = prompt[0]

        # Extract attributes
        name = self._data.get("question_name")
        placeholder = self._data.get("question_placeholder")

        # Modify new fields
        update(prompt, "question_name", name)
        update(prompt, "question_placeholder", placeholder)

        prompt.save()
        return success_response(self._serializer(prompt).data, status.HTTP_200_OK)
        
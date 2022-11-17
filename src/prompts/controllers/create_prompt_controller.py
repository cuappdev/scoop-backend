from api.utils import success_response
from api.utils import failure_response
from prompts.models import Prompt
from rest_framework import status

class CreatePromptController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        name = self._data.get("question_name")
        if name is None:
            return failure_response("No name provided.", status.HTTP_400_BAD_REQUEST)
        
        placeholder = self._data.get("question_placeholder")

        prompt = Prompt.objects.filter(question_name=name, question_placeholder=placeholder)
        if prompt:
            return success_response(self._serializer(prompt[0]).data, status.HTTP_200_OK)
        
        prompt = Prompt.objects.create(question_name=name, question_placeholder=placeholder)
        prompt.save()
        return success_response(self._serializer(prompt).data, status.HTTP_201_CREATED)
    

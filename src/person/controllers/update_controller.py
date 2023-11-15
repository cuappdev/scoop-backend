import json

from api.utils import failure_response
from api.utils import success_response
from api.utils import update
from django.contrib.auth.models import User
from prompts.models import Prompt
from fcm_django.models import FCMDevice

from ..utils import remove_profile_pic
from ..utils import upload_profile_pic


class UpdatePersonController:
    def __init__(self, user, data, serializer):
        self._data = data
        self._serializer = serializer
        self._user = user
        self._person = self._user.person

    def process(self):
        netid = self._data.get("netid")
        first_name = self._data.get("first_name")
        last_name = self._data.get("last_name")
        fcm_registration_token = self._data.get("fcm_registration_token")
        grade = self._data.get("grade")
        phone_number = self._data.get("phone_number")
        profile_pic_base64 = self._data.get("profile_pic_base64")
        prompts = self._data.get("prompts")
        pronouns = self._data.get("pronouns")

        if prompts is not None:
            prompts = sorted(prompts, key=lambda x: x["id"])
            prompt_ids = []
            prompt_answers = []

            for prompt in prompts:
                prompt_id = prompt.get("id")
                answer = prompt.get("answer")
                question = Prompt.objects.filter(id=prompt_id)
                if not question:
                    return failure_response(f"Prompt id {prompt_id} does not exist.")
                prompt_ids.append(prompt_id)
                prompt_answers.append(answer)

            self._person.prompt_questions.set(prompt_ids)
            update(self._person, "prompt_answers", json.dumps(prompt_answers))

        if fcm_registration_token is not None and self._person.fcm_registration_token != fcm_registration_token:
            FCMDevice.objects.filter(
                registration_id=self._person.fcm_registration_token
            ).delete()
            self._person.fcm_registration_token = fcm_registration_token
            fcm_device = FCMDevice.objects.create(
                registration_id=fcm_registration_token,
                cloud_message_type="FCM",
                user=self._user,
            )
            self._user.fcm_device = fcm_device

        update(self._person, "netid", netid)
        update(self._user, "first_name", first_name)
        update(self._user, "last_name", last_name)
        update(self._person, "grade", grade)
        update(self._person, "phone_number", phone_number)
        update(self._person, "pronouns", pronouns)

        self._user.save()
        self._person.save()

        if profile_pic_base64 == "":
            remove_profile_pic(self._user.id)
        elif profile_pic_base64 is not None:
            upload_profile_pic(self._user.id, profile_pic_base64)

        self._user = User.objects.get(id=self._user.id)
        return success_response(self._serializer(self._user).data)

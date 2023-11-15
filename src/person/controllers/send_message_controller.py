from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from rest_framework import status


class SendMessageController:
    def __init__(self, user, data, receiving_user_id):
        self._user = user
        self._data = data
        self._receiving_user_id = receiving_user_id

    def process(self):
        message = self._data.get("message")
        if not message:
            return failure_response("Message is required", status.HTTP_400_BAD_REQUEST)
        receiving_user = User.objects.filter(id=self._receiving_user_id)
        if not receiving_user:
            return failure_response(
                "Receiving user not found", status.HTTP_404_NOT_FOUND
            )
        receiving_user = receiving_user[0]
        if not receiving_user.person.fcm_registration_token:
            # Receiving user does not have notifications enabled, but message will still be delivered through Firebase
            # device = FCMDevice()
            # device.registration_id = ...
            return success_response(status=status.HTTP_200_OK)
        device = FCMDevice.objects.get(
            registration_id=receiving_user.person.fcm_registration_token
        )
        response = device.send_message(
            Message(
                notification=Notification(
                    title=f"New Ride Request from {self._user.first_name}", body=message
                )
            )
        )
        if response.get("failure") == 1:
            return failure_response(
                f"Failed to send message, FCM Response: {response}",
                status.HTTP_502_BAD_GATEWAY,
            )
        return success_response(status=status.HTTP_201_CREATED)

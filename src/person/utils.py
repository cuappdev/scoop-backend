from os import environ

from api.utils import failure_response
from django.contrib.auth.models import User
import requests


def upload_profile_pic(user_id, profile_pic_base64):
    """Uploads image to server and modifies user's profile_pic_url"""
    request_body = {
        "bucket": environ.get("IMAGE_BUCKET_NAME"),
        "image": profile_pic_base64,
    }
    response = requests.post(environ.get("IMAGE_UPLOAD_URL"), json=request_body).json()
    if not response.get("success"):
        return failure_response("Image upload not successful.")
    user = User.objects.get(id=user_id)
    person = user.person
    person.profile_pic_url = response.get("data")
    user.save()
    person.save()

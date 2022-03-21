from api.settings import IMAGE_BUCKET_NAME
from api.settings import IMAGE_UPLOAD_URL
from api.utils import failure_response
from django.contrib.auth.models import User
import requests


def upload_profile_pic(user_id, profile_pic_base64):
    """Uploads image to server and modifies user's profile_pic_url"""
    request_body = {
        "bucket": IMAGE_BUCKET_NAME,
        "image": profile_pic_base64,
    }
    response = requests.post(IMAGE_UPLOAD_URL, json=request_body)
    if response.status_code != 201:
        return failure_response("Image upload not successful.")
    user = User.objects.get(id=user_id)
    person = user.person
    person.profile_pic_url = response.json().get("data")
    user.save()
    person.save()

from api.settings import IMAGE_BUCKET_NAME
from api.settings import IMAGE_UPLOAD_URL
from django.contrib.auth.models import User
import requests


def upload_profile_pic(user_id, profile_pic_base64):
    """Uploads image to server and modifies user's profile_pic_url"""
    request_body = {
        "bucket": IMAGE_BUCKET_NAME,
        "image": profile_pic_base64,
    }
    response = requests.post(IMAGE_UPLOAD_URL + "upload/", json=request_body)
    if response.status_code != 201:
        return
    user = User.objects.get(id=user_id)
    person = user.person
    if person.profile_pic_url:
        remove_profile_pic(user_id)
    person.profile_pic_url = response.json().get("data")
    user.save()
    person.save()


def remove_profile_pic(user_id):
    """Removes image from server and modifies user's profile_pic_url"""
    user = User.objects.get(id=user_id)
    person = user.person
    request_body = {"bucket": IMAGE_BUCKET_NAME, "image_url": person.profile_pic_url}
    response = requests.post(IMAGE_UPLOAD_URL + "remove/", json=request_body)
    if response.status_code != 200:
        return
    person.profile_pic_url = ""
    user.save()
    person.save()

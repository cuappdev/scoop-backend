from api.settings import IMAGE_BUCKET_NAME
from api.settings import IMAGE_UPLOAD_URL
from django.contrib.auth.models import User
import requests


def upload_profile_pic(user_id, bucket, image_file):
    """Uploads image to server and modifies user's profile_pic_url. Uses form data instead of JSON body."""
    data = { "bucket": bucket }
    files = { "image": image_file }
    response = requests.post(IMAGE_UPLOAD_URL + "upload/", files=files, data=data)
    if response.status_code != 201:
        return
    user = User.objects.get(id=user_id)
    person = user.person
    # if there is already a profile picture, delete old one to free up space on server
    if person.profile_pic_url:
        remove_profile_pic(user_id)
    print(response.json())
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

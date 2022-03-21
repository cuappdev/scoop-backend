from os import environ

from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin

ADMIN_PERMISSIONS = [IsAuthenticated, IsAdmin]

STANDARD_PERMISSIONS = [IsAuthenticated, DjangoModelPermissions]

CONSUMER_PERMISSIONS = [IsAuthenticated]

UNPROTECTED = [AllowAny]

AUTH_PASSWORD_SALT = environ.get("AUTH_PASSWORD_SALT")
ACCESS_TOKEN_AGE = 60 * 15
GOOGLE_DEBUG = environ.get("GOOGLE_DEBUG")
IMAGE_UPLOAD_URL = environ.get("IMAGE_UPLOAD_URL")
IMAGE_BUCKET_NAME = environ.get("IMAGE_BUCKET_NAME")

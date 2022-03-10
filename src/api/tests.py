import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .constants import TEST_EMAIL
from .constants import TEST_FIRSTNAME
from .constants import TEST_LASTNAME


class TestAuthenticate(TestCase):
    AUTHENTICATE_URL = reverse("authenticate")
    FIRST_NAME = TEST_FIRSTNAME
    LAST_NAME = TEST_LASTNAME
    EMAIL = TEST_EMAIL

    def setUp(self):
        self.client = APIClient()

    def test_create_user_and_login(
        self,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        email=EMAIL,
    ):
        """Checks if user is successfully created and auth token is returned."""
        data = {
            "sub": "googleID",
            "given_name": first_name,
            "family_name": last_name,
            "email": email,
        }
        response = self.client.post(self.AUTHENTICATE_URL, data)
        self.assertEqual(response.status_code, 201)
        token = json.loads(response.content)["access_token"]
        self.assertIsNotNone(token)

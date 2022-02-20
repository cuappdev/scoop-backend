from django.urls import re_path
from person.views import AuthenticateView
from person.views import MeView


urlpatterns = [
    re_path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    re_path("me/", MeView.as_view(), name="me"),
]

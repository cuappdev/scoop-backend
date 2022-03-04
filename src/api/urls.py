from django.urls import path
from person.views import AuthenticateView
from person.views import MeView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("me/", MeView.as_view(), name="me"),
]

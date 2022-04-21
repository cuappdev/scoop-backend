from django.urls import path
from person.views import AuthenticateView
from person.views import DeveloperView
from person.views import MeView
from ride.views import AllRidesView
from ride.views import RideView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("dev/", DeveloperView.as_view(), name="dev"),
    path("me/", MeView.as_view(), name="me"),
    path("ride/<int:id>/", RideView.as_view(), name="ride"),
    path("rides/", AllRidesView.as_view(), name="all_rides"),
]

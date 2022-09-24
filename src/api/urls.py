from django.urls import path
from person.views import AuthenticateView
from person.views import DeveloperView
from person.views import MeView
from ride.views import RidesView
from ride.views import RideView
from ride.views import SearchView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("dev/", DeveloperView.as_view(), name="dev"),
    path("me/", MeView.as_view(), name="me"),
    path("rides/<int:id>/", RideView.as_view(), name="ride"),
    path("rides/", RidesView.as_view(), name="rides"),
    path("search/", SearchView.as_view(), name="search")
]

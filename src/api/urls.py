from django.urls import path
from person.views import AuthenticateView
from person.views import DeveloperView
from person.views import MeView
from request.views import RequestsView
from request.views import RequestView
from ride.views import RidesView
from ride.views import RideView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("dev/", DeveloperView.as_view(), name="dev"),
    path("me/", MeView.as_view(), name="me"),
    path("rides/<int:id>/", RideView.as_view(), name="ride"),
    path("rides/", RidesView.as_view(), name="rides"),
    path("requests/<int:id>/", RequestView.as_view(), name="request"),
    path("requests/", RequestsView.as_view(), name="requests"),
]

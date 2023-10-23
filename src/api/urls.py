from django.urls import include
from django.urls import path
from django.urls import re_path
from person.views import AuthenticateView
from person.views import DeveloperView
from person.views import MeView
from person.views import BlockView
from person.views import UnblockView
from ride.views import RidesArchiveView
from ride.views import RidesView
from ride.views import RideView
from ride.views import SearchView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("dev/", DeveloperView.as_view(), name="dev"),
    path("me/", MeView.as_view(), name="me"),
    path("block/", BlockView.as_view(), name="block"),
    path("unblock/", UnblockView.as_view(), name="unblock"),
    path("rides/<int:id>/", RideView.as_view(), name="ride"),
    path("rides/", RidesView.as_view(), name="rides"),
    path("rides/archive/", RidesArchiveView.as_view(), name="rides"),
    path("search/", SearchView.as_view(), name="search"),
    re_path(r"^requests/", include("request.urls")),
    re_path(r"^prompts/", include("prompts.urls"))
]

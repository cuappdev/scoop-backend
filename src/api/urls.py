from django.urls import include
from django.urls import path
from django.urls import re_path
from person.views import AuthenticateView
from person.views import DeveloperView
from person.views import MeView
from person.views import SendMessageView
from ride.views import RidesView
from ride.views import RideView
from ride.views import SearchView
from rest_framework_swagger.views import get_swagger_view
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("dev/", DeveloperView.as_view(), name="dev"),
    path("me/", MeView.as_view(), name="me"),
    path("users/<int:id>/message/", SendMessageView.as_view(), name="message"),
    path('devices', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    path("rides/<int:id>/", RideView.as_view(), name="ride"),
    path("rides/", RidesView.as_view(), name="rides"),
    path("search/", SearchView.as_view(), name="search"),
    re_path(r"^requests/", include("request.urls")),
    re_path(r"^prompts/", include("prompts.urls"))
]

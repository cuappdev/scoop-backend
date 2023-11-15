from django.urls import include, path, re_path
from person.views import AuthenticateView
from person.views import DeveloperView
from person.views import MeView
from person.views import SendMessageView
from ride.views import RidesView
from ride.views import RideView
from ride.views import SearchView
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceViewSet

schema_view = get_swagger_view(title='Pastebin API')

router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)

urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("dev/", DeveloperView.as_view(), name="dev"),
    path("me/", MeView.as_view(), name="me"),
    path("users/<int:id>/message/", SendMessageView.as_view(), name="message"),
    path("rides/<int:id>/", RideView.as_view(), name="ride"),
    path("rides/", RidesView.as_view(), name="rides"),
    path("search/", SearchView.as_view(), name="search"),
    re_path(r"^requests/", include("request.urls")),
    re_path(r"^prompts/", include("prompts.urls")),
    re_path(r"^", include(router.urls)),
]

from django.urls import path
from request.views import RequestsView
from request.views import RequestView

urlpatterns = [
    path("<int:id>/", RequestView.as_view(), name="request"),
    path("", RequestsView.as_view(), name="requests"),
]

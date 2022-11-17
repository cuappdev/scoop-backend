from django.urls import path
from prompts.views import PromptsView

urlpatterns = [
    path("", PromptsView.as_view(), name="prompts")
    ]
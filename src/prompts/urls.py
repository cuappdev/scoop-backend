from django.urls import path
from prompts.views import PromptView
from prompts.views import PromptsView

urlpatterns = [
    path("", PromptsView.as_view(), name="prompts"),
    path("<int:id>/", PromptView.as_view(), name="prompt")
    ]
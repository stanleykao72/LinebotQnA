from django.urls import path

from .views import callback

urlpatterns = [
    path("webhook/", webhook, name="webhook"),
]

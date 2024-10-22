from django.urls import path
from .views import MessageAPIView

urlpatterns = [
    path('message/', MessageAPIView.as_view())
]

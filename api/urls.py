from django.urls import path, include
from .views import ActivateAccountView
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/users/activation/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate-account'),
]

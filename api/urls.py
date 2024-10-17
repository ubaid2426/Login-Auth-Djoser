from django.urls import path, include
from .views import ActivateAccountView
from .views import CustomPasswordResetConfirmView
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/users/activation/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('reset_password_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

from django.urls import path, include
from .views import  ActivateAccountView, UserCreateAPIView
# from .views import CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views

# from api import views
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('auth/users/activation/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate-account'),
    path("auth/users/activation/<uidb64>/<token>/", ActivateAccountView.as_view(), name='activate'),
    # path('generate-otp/', views.GenerateOTP.as_view(), name='generate-otp'),
    # path('verify-otp/', views.VerifyOTP.as_view(), name='verify-otp'),
    path('users/', UserCreateAPIView.as_view(), name='user-create'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

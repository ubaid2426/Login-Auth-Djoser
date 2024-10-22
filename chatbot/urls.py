from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet
from django.conf import settings
from django.conf.urls.static import static
from . import views
# Initialize the router
router = DefaultRouter()
router.register(r'message', MessageViewSet, basename='message')

# Define the base urlpatterns first
urlpatterns = [
    # path('message/', include(router.urls)),
    path('message/', views.send_message, name='send_message'),
    path('message/retrieve/', views.get_messages, name='get_messages'),
]

# Append static media file serving in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

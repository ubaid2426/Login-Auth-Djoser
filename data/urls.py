from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from .views import DonationListView, BloodRequestListCreateView, BloodRequestDetailView, DonationHistoryView, NotificationDetailView, NotificationListCreateView, VideoPostListCreateView, VideoPostDetailView, ItemListView, ItemDetailView
from django.conf.urls.static import static
# router = DefaultRouter()
# router.register(r'donation-options', DonationOptionsCategoryViewSet)
urlpatterns = [
    # URL pattern for bottom navigation items
    path('bottom-navigation-items/', views.bottom_navigation_items, name='bottom_navigation_items'),

    # URL pattern for all categories
    path('categories/', views.all_categories, name='all_categories'),
    path('individualcategories/', views.individual_categories, name='individual_categories'),
    path('staticcategories/', views.static_categories, name='static_categories'),

    # URL pattern for donation projects
    path('donations/', DonationListView.as_view(), name='donation-list'),
    path('blood-requests/', BloodRequestListCreateView.as_view(), name='blood-requests-list-create'),
    path('blood-requests/<int:pk>/', BloodRequestDetailView.as_view(), name='blood-request-detail'),
    # URL pattern for working hours
    path('working-hours/', views.working_hours, name='working_hours'),
    path('donor-history/', views.record_donation, name='record_donation'),
    path('donor-history/<int:id>/update-status/', views.update_status, name='update_status'),
    path('donor-history/<int:id>/status/', views.get_donation_status, name='get_donation_status'),
    path('donation-request/', views.create_donation_request, name='create_donation_request'),
    path('donation-history/<int:donor_id>/<str:donor_name>/', DonationHistoryView.as_view(), name='donation-history'),
    path('videos/', VideoPostListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoPostDetailView.as_view(), name='video-detail'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('notifications/', NotificationListCreateView.as_view(), name='notifications-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.urls import path
from . import views
from django.conf import settings
from .views import DonationListView, DonationHistoryView, VideoPostListCreateView, VideoPostDetailView
from django.conf.urls.static import static
urlpatterns = [
    # URL pattern for bottom navigation items
    path('bottom-navigation-items/', views.bottom_navigation_items, name='bottom_navigation_items'),

    # URL pattern for all categories
    path('categories/', views.all_categories, name='all_categories'),

    # URL pattern for donation projects
    path('donations/', DonationListView.as_view(), name='donation-list'),

    # URL pattern for working hours
    path('working-hours/', views.working_hours, name='working_hours'),
    path('donor-history/', views.record_donation, name='record_donation'),
    path('donor-history/<int:id>/update-status/', views.update_status, name='update_status'),
    path('donor-history/<int:id>/status/', views.get_donation_status, name='get_donation_status'),
    path('donation-request/', views.create_donation_request, name='create_donation_request'),
    path('donation-history/<int:donor_id>/<str:donor_name>/', DonationHistoryView.as_view(), name='donation-history'),
    path('videos/', VideoPostListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoPostDetailView.as_view(), name='video-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



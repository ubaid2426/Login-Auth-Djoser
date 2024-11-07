from django.urls import path
from . import views
from django.conf import settings
from .views import DonationListView
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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



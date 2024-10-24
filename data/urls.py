from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for bottom navigation items
    path('bottom-navigation-items/', views.bottom_navigation_items, name='bottom_navigation_items'),

    # URL pattern for all categories
    path('categories/', views.all_categories, name='all_categories'),

    # URL pattern for donation projects
    path('donations/', views.donation_projects, name='donation_projects'),

    # URL pattern for donation project detail (single project)
    path('donations/<uuid:project_id>/', views.donation_project_detail, name='donation_project_detail'),

    # URL pattern for working hours
    path('working-hours/', views.working_hours, name='working_hours'),
]



from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

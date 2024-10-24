from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import AllCategoryModel, DonationModel, BottomNavigationItem, WorkingHours


# Bottom Navigation Items List
def bottom_navigation_items(request):
    items = BottomNavigationItem.objects.all()
    data = [{"disable_icon": item.disable_icon, "anable_icon": item.anable_icon, "label": item.label, "isSelected": item.isSelected} for item in items]
    return JsonResponse(data, safe=False)


# All Categories List
def all_categories(request):
    categories = AllCategoryModel.objects.all()
    data = [{"id": str(category.id), "title": category.title, "image": category.image.url if category.image else None, "route": category.route} for category in categories]
    return JsonResponse(data, safe=False)


# Donation Projects List
# Function to generate image URL
def get_image_url(image_field):
    """Return the URL of the image if it exists; otherwise, return None."""
    return image_field.url if image_field else None



# List View for Donation Projects
def donation_projects(request):
    projects = DonationModel.objects.all()
    data = [{
        "id": str(project.id),
        "title": project.title,
        "description": project.description,
        "project_value": project.project_value,
        "paid_value": project.paid_value,
        "remaining_value": project.remaining_value,
        "date": project.date,
        "image": get_image_url(project.image)  # Use the image URL function here
    } for project in projects]
    
    return JsonResponse(data, safe=False)






# Detail View for Donation Project
def donation_project_detail(request, project_id):
    project = get_object_or_404(DonationModel, id=project_id)
    data = {
        "id": str(project.id),
        "title": project.title,
        "description": project.description,
        "project_value": project.project_value,
        "paid_value": project.paid_value,
        "remaining_value": project.remaining_value,
        "date": project.date,
        "image": get_image_url(project.image)  # Use the image URL function here
    }
    return JsonResponse(data)


# Working Hours View
def working_hours(request):
    working_hours = WorkingHours.objects.all()
    data = [{"title": hours.title, "days": hours.days, "friday": hours.friday} for hours in working_hours]
    return JsonResponse(data, safe=False)

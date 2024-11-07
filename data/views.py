from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import AllCategoryModel, DonationModel, BottomNavigationItem, WorkingHours, DonationHistory
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import DonationSerializer 
from django.db.models import F, ExpressionWrapper, DecimalField
from rest_framework import status
from django.db import models 
from django.utils import timezone
from decimal import Decimal
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


def record_donation(request):
    donation_id = request.GET.get('donation_id')
    donor_name = request.GET.get('donor_name')
    amount = request.GET.get('amount')
    
    
    if not donation_id or not donor_name or not amount:
        return JsonResponse({'error': 'Missing required parameters.'}, status=400)

    try:
        amount = Decimal(amount)
    except ValueError:
        return JsonResponse({'error': 'Invalid amount value.'}, status=400)

    donation = get_object_or_404(DonationModel, id=donation_id)
    donation.update_paid_value(amount)
    DonationHistory.objects.create(
        donation=donation,
        donor_name=donor_name,
        amount=amount,
        date=timezone.now(),
        image=donation.image,
        payment_status='Pending'
    )

    return JsonResponse({'success': 'Donation recorded successfully.'})

class DonationListView(APIView):
    def get(self, request):
        try:
            # Get category from query parameters
            category = request.query_params.get('category', None)
            
            # Get all donations and filter by category if specified
            donations = DonationModel.objects.all()
            if category:
                donations = donations.filter(category__title__iexact=category)

            # Handle sorting and filtering options from query params
            sort_option = request.query_params.get('sort', None)
            filter_option = request.query_params.get('filter', None)

            if filter_option == 'finished':
                donations = donations.filter(paid_value__gte=F('project_value'))
            elif filter_option == 'unfinished':
                donations = donations.filter(paid_value__lt=F('project_value'))
                
            if sort_option == 'oldest':
                donations = donations.order_by('date')
            elif sort_option == 'newest':
                donations = donations.order_by('-date')
            elif sort_option == 'remaining_low_to_high':
                # Annotate with the remaining value
                donations = donations.annotate(
                    remaining_value=ExpressionWrapper(
                        F('project_value') - F('paid_value'),
                        output_field=DecimalField()
                    )
                ).order_by('remaining_value')
            elif sort_option == 'remaining_high_to_low':
                donations = donations.annotate(
                    remaining_value=ExpressionWrapper(
                        F('project_value') - F('paid_value'),
                        output_field=DecimalField()
                    )
                ).order_by('-remaining_value')

            # Serialize the data
            serializer = DonationSerializer(donations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Error occurred: {e}")  # Log the error for debugging
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Detail View for Donation Project
# def donation_project_detail(request, project_id):
#     project = get_object_or_404(DonationModel, id=project_id)
#     data = {
#         "id": str(project.id),
#         "title": project.title,
#         "description": project.description,
#         "project_value": project.project_value,
#         "paid_value": project.paid_value,
#         "remaining_value": project.remaining_value,
#         "date": project.date,
#         "image": get_image_url(project.image)  # Use the image URL function here
#     }
#     return JsonResponse(data)


# Working Hours View
def working_hours(request):
    working_hours = WorkingHours.objects.all()
    data = [{"title": hours.title, "days": hours.days, "friday": hours.friday} for hours in working_hours]
    return JsonResponse(data, safe=False)

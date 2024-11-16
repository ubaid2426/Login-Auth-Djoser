import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import AllCategoryModel, DonationModel, BottomNavigationItem, WorkingHours, DonationHistory
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import DonationSerializer, DonationRequestSerializer, DonationHistorySerializer 
from django.db.models import F, ExpressionWrapper, DecimalField
from rest_framework import status
from django.db import models 
from django.utils import timezone
from django.middleware.csrf import get_token
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# import base64
# from io import BytesIO
# from django.core.files.base import ContentFile
# Bottom Navigation Items List
def bottom_navigation_items(request):
    items = BottomNavigationItem.objects.all()
    data = [{"disable_icon": item.disable_icon, "anable_icon": item.anable_icon, "label": item.label, "isSelected": item.isSelected} for item in items]
    return JsonResponse(data, safe=False)
def my_view(request):
    csrf_token = get_token(request)
    print(csrf_token)
    return HttpResponse("CSRF token generated!")

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


class DonationHistoryView(APIView):
    def get(self, request, donor_id, donor_name):
        # Fetch donation history records for the given donor ID and name
        donation_history = DonationHistory.objects.filter(
            donor_id=donor_id,
            donor_name=donor_name
        )

        # Serialize the data
        serializer = DonationHistorySerializer(donation_history, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
def record_donation(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    try:
        # Parse JSON data from the request body
        donor_id = request.POST.get('donor_id')
        donor_name = request.POST.get('donor_name')
        amount = request.POST.get('amount')
        donation_title = request.POST.get('donation_title')
        is_zakat = request.POST.get('is_zakat')
        is_sadqah = request.POST.get('is_sadqah')
        payment_image = request.FILES.get('payment_image')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid JSON or missing required parameters.'}, status=400)

    # Check for missing parameters
    if not all([donor_name, amount, donation_title, payment_image]):
        return JsonResponse({'error': 'Missing required parameters.'}, status=400)
    # Convert amount to Decimal
    def convert_to_bool(value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            raise ValueError("Invalid value for boolean conversion")
    
    try:
        # Convert the string values to booleans
        is_zakat = convert_to_bool(is_zakat)
        is_sadqah = convert_to_bool(is_sadqah)
    except ValueError:
        return JsonResponse({'error': 'Invalid is_zakat or is_sadqah value.'}, status=400)

    # Convert amount to Decimal
    try:
        amount = Decimal(amount)
    except ValueError:
        return JsonResponse({'error': 'Invalid amount value.'}, status=400)

    # Get the donation object
    donation = get_object_or_404(DonationModel, title=donation_title)
    donation.update_paid_value(amount)

    # Create the DonationHistory record
    DonationHistory.objects.create(
        donation=donation,
        donor_name=donor_name,
        is_zakat=is_zakat,
        is_sadqah=is_sadqah,
        donor_id=donor_id,
        amount=amount,
        date=timezone.now(),
        Payment_image=payment_image,
        image=donation.image,
        payment_status='Pending'
    )

    return JsonResponse({'success': 'Donation recorded successfully.'})



@api_view(['POST'])
def create_donation_request(request):
    serializer = DonationRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def update_status(request, id):
    if request.method == 'POST':
        new_status = request.POST.get('payment_status')
        if new_status in ['Completed', 'Pending']:
            try:
                donation = DonationHistory.objects.get(id=id)
                donation.payment_status = new_status
                donation.save()
                return JsonResponse({'success': 'Status updated successfully.'})
            except DonationHistory.DoesNotExist:
                return JsonResponse({'error': 'Donation record not found.'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid status provided.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def get_donation_status(request, id):
    # Retrieve all DonationHistory records for the donor_id
    donations = DonationHistory.objects.filter(donor_id=id).order_by('-date')
    # donation = get_object_or_404(DonationModel, title=donation_title)
    if donations.exists():
        # Return the latest payment status if only one status is needed
        latest_donation = donations.first()
        return JsonResponse({
            # 'title': 
            'donor_id': latest_donation.donor_id,
            'payment_status': latest_donation.payment_status
        })
        
        # Or, to return all records, uncomment the following and remove the code above
        # return JsonResponse({
        #     'donor_id': id,
        #     'payment_statuses': [
        #         {'date': donation.date, 'status': donation.payment_status} for donation in donations
        #     ]
        # })
    else:
        return JsonResponse({'error': 'No donation records found for this donor.'}, status=404)

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

import json
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import AllCategoryModel, DonationModel, BottomNavigationItem, WorkingHours, DonationHistory, VideoPost
from rest_framework.views import APIView
from django.http import StreamingHttpResponse, Http404
from wsgiref.util import FileWrapper
from rest_framework.response import Response
from .serializer import DonationSerializer, DonationRequestSerializer, DonationHistorySerializer, VideoPostSerializer 
from django.db.models import F, ExpressionWrapper, DecimalField
from rest_framework import status
from django.db.models import Sum, Count
from django.utils import timezone
from django.middleware.csrf import get_token
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
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

        # Calculate totals and counts
        total_amount = donation_history.aggregate(Sum('amount'))['amount__sum'] or 0
        total_donations = donation_history.count()
        zakat_count = donation_history.filter(is_zakat=True).count()
        sadqah_count = donation_history.filter(is_sadqah=True).count()

        # Serialize the donation history data
        serializer = DonationHistorySerializer(donation_history, many=True)

        # Send payment_status as part of the response
        response_data = {
            "donation_history": serializer.data,
            "total_amount": total_amount,
            "total_donations": total_donations,
            "zakat_count": zakat_count,
            "sadqah_count": sadqah_count,
        }

        # Return the serialized data
        return Response(response_data, status=status.HTTP_200_OK)



@csrf_exempt
def record_donation(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    try:
        # Parse the JSON payload from the `data` field
        data = json.loads(request.POST['data'])
        print(data);
        donor_id = data.get('donor_id')
        donor_name = data.get('donor_name')
        donations = data.get('donations', [])
        donations1 = data.get('donations1', [])
        donation_titles = data.get('donation_title', [])
        is_zakat_list = data.get('is_zakat', [])
        is_sadqah_list = data.get('is_sadqah', [])
        # quantity=
        # Get the payment image file
        payment_image = request.FILES.get('payment_image')

        # Validate required fields
        if not all([donor_id, donor_name, donations, donations1, donation_titles]):
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        # Process donations here
        for i, donation in enumerate(donations):
            amount = donation.get('amount', 0)
            quantity = donations1[i].get('quantity', 0)
            title = donation_titles[i].get('donation_title')
            is_zakat = is_zakat_list[i].get('isZakat', False)
            is_sadqah = is_sadqah_list[i].get('isSadqah', False)
            print(amount);
            print(quantity);
            print(title);
            print(is_zakat);
            print(is_sadqah);
            donation = get_object_or_404(DonationModel, title=title)
            # donation.update_paid_value(amount)
            # donation.update_paid_value(quantity)
            if quantity > 0:
                donation.update_paid_value(quantity)
            elif amount > 0:
                donation.update_paid_value(amount)
            DonationHistory.objects.create(
                donation=donation,
                donor_name=donor_name,
                quantity=quantity,
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
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)
    except UnicodeDecodeError as e:
        return JsonResponse({'error': f'Encoding issue: {str(e)}'}, status=400)





class VideoPostListCreateView(APIView):
    """
    Handles listing all video posts and creating new video posts.
    """
    def get(self, request):
        posts = VideoPost.objects.all()
        serializer = VideoPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VideoPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoPostDetailView(APIView):
    """
    Handles retrieving a specific video post and streaming its video content.
    """

    def get(self, request, pk):
        # Retrieve the video post by ID
        post = get_object_or_404(VideoPost, pk=pk)
        serializer = VideoPostSerializer(post)

        # Video file path from the VideoPost model
        video_path = post.video.path  # Ensure `video` is the field name for the file in the VideoPost model

        # Check if the video file exists
        if not os.path.exists(video_path):
            return Response({"error": "Video file not found"}, status=status.HTTP_404_NOT_FOUND)

        # Open the video file in binary read mode
        try:
            file_handle = open(video_path, 'rb')
            file_wrapper = FileWrapper(file_handle)
            file_size = os.path.getsize(video_path)

            # Create a StreamingHttpResponse using FileWrapper
            response = StreamingHttpResponse(file_wrapper, content_type='video/mp4')
            response['Content-Length'] = file_size
            response['Content-Disposition'] = 'inline'  # Optional, ensures video plays in the browser
            return response

        except IOError:
            raise Http404("Error opening the video file.")

    def delete(self, request, pk):
        # Delete the specified video post
        try:
            post = VideoPost.objects.get(pk=pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except VideoPost.DoesNotExist:
            return Response({"error": "VideoPost not found"}, status=status.HTTP_404_NOT_FOUND)


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
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            new_status = data.get('payment_status')

            # Validate status
            if new_status not in ['Pending', 'Completed']:
                return JsonResponse({'error': 'Invalid status provided.'}, status=400)

            # Update donation record
            donation = DonationHistory.objects.get(id=id)
            donation.payment_status = new_status
            donation.save()

            return JsonResponse({'success': 'Status updated successfully.'})

        except DonationHistory.DoesNotExist:
            return JsonResponse({'error': 'Donation record not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

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
    else:
        return JsonResponse({'error': 'No donation records found for this donor.'}, status=404)

# class DonationListView(APIView):
#     def get(self, request):
#         try:
#             # Get category from query parameters
#             category = request.query_params.get('category', None)
#             category_select = request.query_params.get('category_select', None)
#             # Get all donations and filter by category if specified
#             donations = DonationModel.objects.all()
#             if category:
#                 donations = donations.filter(category__title__iexact=category)
#             if category_select:
#                 donations = donations.filter(category_select__title__iexact=category_select)

#             # Handle sorting and filtering options from query params
#             sort_option = request.query_params.get('sort', None)
#             filter_option = request.query_params.get('filter', None)

#             if filter_option == 'finished':
#                 donations = donations.filter(paid_value__gte=F('project_value'))
#             elif filter_option == 'unfinished':
#                 donations = donations.filter(paid_value__lt=F('project_value'))
                
#             if sort_option == 'oldest':
#                 donations = donations.order_by('date')
#             elif sort_option == 'newest':
#                 donations = donations.order_by('-date')
#             elif sort_option == 'remaining_low_to_high':
#                 # Annotate with the remaining value
#                 donations = donations.annotate(
#                     remaining_value=ExpressionWrapper(
#                         F('project_value') - F('paid_value'),
#                         output_field=DecimalField()
#                     )
#                 ).order_by('remaining_value')
#             elif sort_option == 'remaining_high_to_low':
#                 donations = donations.annotate(
#                     remaining_value=ExpressionWrapper(
#                         F('project_value') - F('paid_value'),
#                         output_field=DecimalField()
#                     )
#                 ).order_by('-remaining_value')

#             # Serialize the data
#             serializer = DonationSerializer(donations, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             print(f"Error occurred: {e}")  # Log the error for debugging
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class DonationListView(APIView):
    def get(self, request):
        try:
            # Get query parameters
            category = request.query_params.get('category', None)
            category_select = request.query_params.get('category_select', None)

            # Get all donations and apply filters
            donations = DonationModel.objects.all()
            if category:
                donations = donations.filter(category__title__iexact=category)
            if category_select:
                donations = donations.filter(category_select__title__iexact=category_select)

            # Handle sorting and filtering options
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

# Working Hours View
def working_hours(request):
    working_hours = WorkingHours.objects.all()
    data = [{"title": hours.title, "days": hours.days, "friday": hours.friday} for hours in working_hours]
    return JsonResponse(data, safe=False)

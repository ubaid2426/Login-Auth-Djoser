import json
import os
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework import generics
from .models import BloodRequest
from api.models import User
from loginauth import settings
from .models import AllCategoryModel, IndividualCategory, Item, DonationModel, BottomNavigationItem, Notification, StaticCategory, WorkingHours, DonationHistory, VideoPost
from rest_framework.views import APIView
from django.http import StreamingHttpResponse, Http404
from rest_framework.response import Response
from .serializer import DonationSerializer, BloodRequestSerializer, NotificationSerializer, ItemSerializer, DonationRequestSerializer, DonationHistorySerializer, VideoPostSerializer 
from django.db.models import F, ExpressionWrapper, DecimalField
from rest_framework import status, generics
from django.db.models import Sum, Count
from django.utils import timezone
from django.middleware.csrf import get_token
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
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
def individual_categories(request):
    individual_categories = IndividualCategory.objects.all()
    individual_data = [{"id": str(individual_category.id), "title": individual_category.title, "image": individual_category.image.url if individual_category.image else None, "route": individual_category.route} for individual_category in individual_categories]
    return JsonResponse(individual_data, safe=False)
def static_categories(request):
    static_categories = StaticCategory.objects.all()
    static_data = [{"id": str(static_category.id), "title": static_category.title, "image": static_category.image.url if static_category.image else None, "route": static_category.route} for static_category in static_categories]
    return JsonResponse(static_data, safe=False)

class ItemListView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
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
        email_user=data.get('email')
        donor_id = data.get('donor_id')
        donor_name = data.get('donor_name')
        donations = data.get('donations', [])
        donations1 = data.get('donations1', [])
        donation_titles = data.get('donationtitle', [])
        head_categories = data.get('headingcategory', [])
        select_categories = data.get('selectcategory', [])
        gender_selects = data.get('gender', [])
        age_selects = data.get('age', [])
        is_zakat_list = data.get('is_zakat', [])
        is_sadqah_list = data.get('is_sadqah', [])
        # quantity=
        # Get the payment image file
        payment_image = request.FILES.get('payment_image')

        # Validate required fields
        if not all([donor_id, donor_name, donations, donations1, email_user]):
            return JsonResponse({'error': 'Missing required fields.'}, status=405)
        try:
            user=User.objects.get(email=email_user)
        except User.DoesNotExist:
            raise ValidationError({"email": "User with this email doesn't exist"})
        # Process donations here
        for i, donation in enumerate(donations):
            amount = donation.get('amount', 0)
            quantity = donations1[i].get('quantity', 0)
            title = donation_titles[i].get('donationtitle')
            heading_category = head_categories[i].get('headingcategory')
            gender = gender_selects[i].get('gender')
            age = age_selects[i].get('age')
            select_category = select_categories[i].get('selectcategory')
            is_zakat = is_zakat_list[i].get('isZakat', False)
            is_sadqah = is_sadqah_list[i].get('isSadqah', False)
            print(amount);
            print(quantity);
            print(title);
            print(is_zakat);
            print(is_sadqah);
            try:
                donation = DonationModel.objects.get(title=title)
            except DonationModel.DoesNotExist:
                donation = None  # Set to None if not found            
            # donation = get_object_or_404(DonationModel, title=title)
            if donation:
                if quantity > 0:
                    donation.update_paid_value(quantity)
                elif amount > 0:
                    donation.update_paid_value(amount)
            DonationHistory.objects.create(
                donation=donation,
                donor_name=donor_name,
                quantity=quantity,
                heading_category=heading_category,
                gender=gender,
                age=age,
                email=user,
                select_category=select_category,
                is_zakat=is_zakat,
                is_sadqah=is_sadqah,
                donor_id=donor_id,
                amount=amount,
                date=timezone.now(),
                Payment_image=payment_image,
                image=donation.image,
                payment_status='Pending'
            )
            Notification.objects.create(user=user, title="Donation Successful", message=f"Your donation of {amount} has been successfully processed and payment status 'Pending'.")

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
        data = json.loads(request.body)
        title=data.get("title")
        if serializer.is_valid():
            # Save the new video post
            all_users = User.objects.all()
            print(all_users)
            title=title,
            message = "A new reel has been added."
              # Use map to create notifications for all users
            list(map(lambda user: Notification.objects.create(user=user, message=message), all_users))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoPostDetailView(APIView):
    """
    Handles retrieving a specific video post and serving its HLS/DASH manifest.
    """

    def get(self, request, pk):
        # Retrieve the video post by ID
        post = get_object_or_404(VideoPost, pk=pk)
        serializer = VideoPostSerializer(post)

        # Path to HLS or DASH manifest file (adjust field names as necessary)
        hls_manifest_path = os.path.join(post.video.path, 'output.m3u8')
        dash_manifest_path = os.path.join(post.video.path, 'output.mpd')

        # Check if HLS or DASH manifest exists
        if os.path.exists(hls_manifest_path):
            manifest_path = hls_manifest_path
            content_type = 'application/vnd.apple.mpegurl'  # HLS MIME type
        elif os.path.exists(dash_manifest_path):
            manifest_path = dash_manifest_path
            content_type = 'application/dash+xml'  # DASH MIME type
        else:
            return Response({"error": "Manifest file not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serve the manifest file
        try:
            return FileResponse(open(manifest_path, 'rb'), content_type=content_type)
        except IOError:
            raise Http404("Error opening the manifest file.")

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
    data = json.loads(request.POST['data'])
    email_user=data.get('email')
    try:
        user=User.objects.get(email=email_user)
    except User.DoesNotExist:
        raise ValidationError({"email": "User with this email doesn't exist"})
    if serializer.is_valid():
        serializer.save()
        Notification.objects.create(user=user, message="Your donation request has been successfully processed and team will investigate on it.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
def update_status(request, id):
    if request.method == 'POST':
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            new_status = data.get('payment_status')
            email_user=data.get('email')
            # Validate status
            if new_status not in ['Pending', 'Completed']:
                return JsonResponse({'error': 'Invalid status provided.'}, status=400)
            
            # Update donation record
            donation = DonationHistory.objects.get(id=id)
            user_mail = DonationHistory.objects.get(email=email_user)
            donation.payment_status = new_status
            donation.save()

            message = f"Your payment status is now: {new_status}."
            Notification.objects.create(user=user_mail, message=message)
            

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



# List and Create View for BloodRequest
class BloodRequestListCreateView(generics.ListCreateAPIView):
    queryset = BloodRequest.objects.all().order_by('-created_at')
    serializer_class = BloodRequestSerializer

# Retrieve, Update, and Delete View for BloodRequest
class BloodRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer

class NotificationListCreateView(APIView):
    """
    List all notifications or create a new notification.
    """
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationDetailView(APIView):
    """
    Retrieve, update, or delete a notification instance.
    """
    def get(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            serializer = NotificationSerializer(notification)
            return Response(serializer.data)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            serializer = NotificationSerializer(notification, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import serializers
from .models import DonationImage, IndividualDonorRequest, DonationModel, DonationRequest, DonationHistory, Notification, VideoPost, Item




class DonationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationImage
        fields = ['id', 'images']
class DonationSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    # donation_options = DonationOptionSerializer(many=True)
    images = DonationImageSerializer(many=True, read_only=True)
    class Meta:
        model = DonationModel
        fields = ['id', 'project_id', 'title', 'images', 'title_notice', 'latitude', 'longitude', 'address', 'image', 'description', 'project_value', 'paid_value', 'category', 'category_select', 'date', 'position']

# from rest_framework import serializers
from .models import BloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = ['id', 'name', 'contact_number', 'blood_type', 'distance_km', 'time_required', 'quantity', 'created_at']

class IndividualDonorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualDonorRequest
        fields = ['id', 'name', 'contact_number', 'optional', 'current_location', 'donation_type', 'amount']

# class DonationOptionsCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DonationOptionsCategory
#         fields = ['id', 'title', 'price', 'category', 'category_select']



class DonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = [
            'name', 'phone', 'amount_required', 'description', 'street_address', "email",
            'apartment', 'city', 'state', 'country', 'is_zakat', 'is_sadqah', 'created_at'
        ]
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'image', 'text1', 'text2', 'detail']

class DonationHistorySerializer(serializers.ModelSerializer):

    title = serializers.CharField(source="donation.title", read_only=True)
    age = serializers.CharField( read_only=True, default="")
    gender = serializers.CharField( read_only=True, default="Unknown")
    headingcategory = serializers.CharField( read_only=True, default="Unknown")
    selectcategory = serializers.CharField( read_only=True, default="Unknown")
    image = serializers.ImageField(source="donation.image", read_only=True, default=None)
    email=serializers.EmailField( read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source="amount")
    isZakat = serializers.BooleanField(source="is_zakat", read_only=True)
    isSadqah = serializers.BooleanField(source="is_sadqah", read_only=True)
    dateTime = serializers.DateTimeField(source="date", read_only=True)
    
    class Meta:
        model = DonationHistory
        fields = ['title', 'image', 'email', 'price', 'age', 'gender', 'headingcategory', 'selectcategory', 'isZakat', 'isSadqah', 'dateTime', 'payment_status',]    




class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPost
        fields = ['id', 'title', 'description', 'video', 'created_at']





class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
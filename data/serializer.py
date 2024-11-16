from rest_framework import serializers
from .models import DonationModel, DonationRequest, DonationHistory

class DonationSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    # donation_options = DonationOptionSerializer(many=True)
    class Meta:
        model = DonationModel
        fields = ['id', 'title', 'image', 'description', 'project_value', 'paid_value', 'category', 'date', 'position']


# class DonationOptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DonationOption
#         fields = ['id', 'title', 'price']


class DonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = [
            'name', 'phone', 'amount_required', 'description', 'street_address',
            'apartment', 'city', 'state', 'country', 'is_zakat', 'is_sadqah', 'created_at'
        ]


class DonationHistorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="donation.title", read_only=True)
    imageUrl = serializers.ImageField(source="image", read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source="amount")
    isZakat = serializers.BooleanField(source="is_zakat", read_only=True)
    isSadqah = serializers.BooleanField(source="is_sadqah", read_only=True)
    dateTime = serializers.DateTimeField(source="date", read_only=True)

    class Meta:
        model = DonationHistory
        fields = ['title', 'imageUrl', 'price', 'isZakat', 'isSadqah', 'dateTime']        
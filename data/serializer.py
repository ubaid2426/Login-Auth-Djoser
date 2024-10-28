from rest_framework import serializers
from .models import DonationModel

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
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer
from api.models import User
from rest_framework import serializers
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields=('id', 'email', 'name', 'whatsapp_number', 'nationality', 'residense', 'contact_number', 'password')
        
    def create(self, validated_data):
        user = super().create(validated_data)
        # Generate token and uuid logic here so that
        return {
            'uid': user.id,  # Assuming user.id is your UUID
            'token': user.activation_token,  # Make sure to generate this in your user model 
        }     

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'whatsapp_number', 'nationality', 'residense', 'contact_number']
# class OTPSerializer(serializers.Serializer):
#     otp = serializers.CharField(max_length=6)
#     email = serializers.EmailField()
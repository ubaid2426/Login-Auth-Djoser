from djoser.serializers import UserCreateSerializer
from api.models import User
from rest_framework import serializers
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model=User
        fields=('id', 'email', 'name', 'password')
        
    def create(self, validated_data):
        user = super().create(validated_data)
        # Generate token and uuid logic here so that
        return {
            'uid': user.id,  # Assuming user.id is your UUID
            'token': user.activation_token,  # Make sure to generate this in your user model 
        }     

      
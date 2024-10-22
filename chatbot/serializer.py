from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'text', 'image', 'video', 'timestamp']
    
    
    
    
    def create(self, validated_data):
        print(f"Validated Data: {validated_data}")  # Debugging step
        return super().create(validated_data)
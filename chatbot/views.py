from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import Message
from .serializer import MessageSerializer
from rest_framework.response import Response
from django.db import models
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle message creation, listing, and retrieval.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Ensure parsers for media uploads are set

    def get_queryset(self):
        """
        Filter the queryset based on whether the user is staff or a regular user.
        """
        user = self.request.user
        if user.is_staff:
            # Admin can see all messages
            return Message.objects.all().order_by('timestamp')
        else:
            # Regular users can only see their own messages
            return Message.objects.filter(
                models.Q(sender=user) | models.Q(receiver=user)
            ).order_by('timestamp')

    def perform_create(self, serializer):
        """
        Customize the saving logic to assign an admin as the receiver if the sender is a regular user.
        """
        sender = self.request.user
        text = self.request.data.get('text', '')
        image = self.request.FILES.get('image')
        video = self.request.FILES.get('video')

        # Ensure the receiver is the first available admin if the sender is not an admin
        receiver = User.objects.filter(is_staff=True).first()

        if receiver:
            serializer.save(sender=sender, receiver=receiver, text=text, image=image, video=video)
        else:
            raise ValidationError("Admin user not found.")

    def create(self, request, *args, **kwargs):
        """
        Override create method to customize the response message depending on the media type.
        """
        response = super().create(request, *args, **kwargs)
        if 'image' in request.FILES:
            return Response({"message": "Image message sent successfully"}, status=status.HTTP_201_CREATED)
        elif 'video' in request.FILES:
            return Response({"message": "Video message sent successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Text message sent successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def send_message(request):
    """
    API view to handle message creation from regular users.
    """
    if request.method == 'POST':
        # Extract sender from request user (must be authenticated)
        sender = request.user
        
        # Assuming the message is sent to an admin (you can adjust this logic)
        receiver = User.objects.filter(is_admin=True).first()
        
        if not receiver:
            return Response({"error": "No admin available to receive messages."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the message data
        message_data = {
            'sender': sender.id,  # Pass the sender's ID
            'receiver': receiver.id,  # Pass the admin's ID as the receiver
            'text': request.data.get('text'),
            'image': request.FILES.get('image'),
            'video': request.FILES.get('video')
        }
        
        # Serialize the data and validate
        serializer = MessageSerializer(data=message_data)
        
        if serializer.is_valid():
            # Save the message to the database
            serializer.save()

            # Return a 200 OK response with the saved message data
            return Response({"message": "Message sent successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            # Return a 400 response if there's a validation error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Return 405 if the request method is not POST
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_messages(request):
    """
    API view to retrieve all messages (admin view).
    """
    if request.method == 'GET':
        messages = Message.objects.all()  # Adjust according to your needs
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_user_conversation(request, user_id):
    """
    Retrieve the conversation between a specific user and the admin.
    """
    user = User.objects.get(id=user_id)
    messages = Message.get_conversation(user)
    serialized_messages = [
        {
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'text': message.text,
            'image': message.image.url if message.image else None,
            'video': message.video.url if message.video else None,
            'timestamp': message.timestamp
        } 
        for message in messages
    ]
    return JsonResponse(serialized_messages, safe=False)


def admin_message_list(request):
    """
    View to render the list of messages for admin users.
    """
    admin_user = request.user
    messages = Message.objects.filter(receiver=admin_user)
    return render(request, 'admin_messages.html', {'messages': messages})

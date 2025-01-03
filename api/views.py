import random
from venv import logger
from charset_normalizer import from_bytes
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.utils.encoding import force_str
# from djoser.utils import decode_uid, User
from djoser.conf import settings as djoser_settings
# from django.core.mail import send_mail
from api.models import User

from django.utils.crypto import get_random_string

from api.serializers import UserCreateSerializer



class UserCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            # Decode the UID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = self.get_user(uid)
            if user is not None and default_token_generator.check_token(user, token):
               logger.debug("Token is valid")
            else:
               logger.debug("Token is invalid") 
            # Check if the user exists and the token is valid
            if user is not None and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                # Render a success page
                return render(request, "activation_confirm.html", {"user": user})
            else:
                # Render an error page
                return render(request, "activation_error.html", {"error": "Activation link is invalid."})
        except Exception as e:
            return render(request, "activation_error.html", {"error": str(e)})

    def get_user(self, uid):
        try:
            user=get_user_model().objects.get(pk=uid)
            print(user)
            return get_user_model().objects.get(pk=uid)
        except get_user_model().DoesNotExist:
            return None


class CustomPasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            # Decode the UID from base64
            uid = urlsafe_base64_decode(uidb64).decode()
            user = self.get_user(uid)
            
            # Validate the token
            if user is not None and default_token_generator.check_token(user, token):
                new_password = request.data.get('new_password')
                re_new_password = request.data.get('re_new_password')

                # Check if passwords match
                if new_password != re_new_password:
                    return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

                # Set and save the new password
                user.set_password(new_password)
                user.save()

                return Response({'success': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Helper method to get user by uid
def get_user(self, uid, token):
    try:
        user = get_user_model().objects.get(pk=uid)
        # Check if the token is valid for the user
        if default_token_generator.check_token(user, token):
            return user
        else:
            return None
    except get_user_model().DoesNotExist:
        return None



        
class CustomPasswordResetView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid email'}, status=400)

        uidb64 = urlsafe_base64_decode(from_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Send the uidb64 and token in the response
        return JsonResponse({'uid': uidb64, 'token': token}, status=200)

        



        

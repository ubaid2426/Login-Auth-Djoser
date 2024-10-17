from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.http import JsonResponse
from django.utils.encoding import force_str
class ActivateAccountView(APIView):
    # This allows any user (even unauthenticated) to access this view
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = self.get_user(uid)
            if user is not None and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'detail': "Account activated successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "Activation link is invalid."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_user(self, uid):
        try:
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







# class CustomPasswordResetConfirmView(APIView):
#     def post(self, request, uidb64, token):
#         try:
#             # Decode the UID
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = self.get_user(uid)
            
#             # Check if the token is valid
#             if user is not None and default_token_generator.check_token(user, token):
#                 new_password = request.data.get('new_password')
#                 re_new_password = request.data.get('re_new_password')

#                 # Validate new passwords
#                 if new_password != re_new_password:
#                     return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

#                 # Set and save the new password
#                 user.set_password(new_password)
#                 user.save()

#                 return Response({'success': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     def get_user(self, uid):
#         try:
#             return get_user_model().objects.get(pk=uid)
#         except get_user_model().DoesNotExist:
#             return None
        
        
        
class CustomPasswordResetView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid email'}, status=400)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Send the uidb64 and token in the response
        return JsonResponse({'uid': uidb64, 'token': token}, status=200)

        
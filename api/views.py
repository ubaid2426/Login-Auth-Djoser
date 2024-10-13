from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

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

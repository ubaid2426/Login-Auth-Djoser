# # from urllib import request
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.exceptions import ValidationError
# from api.models import User
# from .models import DonationHistory, Notification

# @receiver(post_save, sender=DonationHistory)
# def create_notification(sender, instance, created, email, **kwargs):
#     """
#     Automatically create notifications based on the status of a DonationHistory object.
#     """
#     if not created:  # This means it's an update, not a new record
#         if instance.payment_status == "Pending":
#             message = "Your payment is pending."
#         elif instance.payment_status == "Completed":
#             message = "Your payment has been completed successfully."
#         else:
#             message = None

#         if message:
#             try:
#                 user_mail = sender.objects.get('email')
#                 print(user_mail)
#                 user=User.objects.get(email=user_mail)
#             except User.DoesNotExist:
#                 raise ValidationError({"email": "User with this email doesn't exist"})
#             # Check if the user is authenticated or use 'instance.donor' if applicable
#             # if user.is_authenticated:
#             Notification.objects.create(user=user, message=message)
#             # else:
#                 # Handle anonymous user case (e.g., log a message or redirect to login)
#                 # print("Notification creation skipped for anonymous user.")

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from api.models import User  # Update with your actual User model path
from .models import DonationHistory, Notification, VideoPost

@receiver(post_save, sender=DonationHistory)
# @receiver(post_save, sender=VideoPost)
def create_notification(sender, instance, created, **kwargs):
    """
    Automatically create notifications based on the status of a DonationHistory object.
    """
    if not created:  # Trigger only on updates, not on creation
        # Determine the appropriate message based on payment_status
        if instance.payment_status == "Pending":
            title="Payment Clearance"
            message = "Your payment is pending."
        elif instance.payment_status == "Completed":
            title="Payment Clearance"
            message = "Your payment has been completed successfully."
        else:
            message = None

        if message:
            try:
                # Fetch the associated user based on the email in DonationHistory
                user = User.objects.get(email=instance.email)
            except User.DoesNotExist:
                raise ValidationError({"email": "User with this email does not exist."})

            # Create a notification for the user
            Notification.objects.create(user=user, message=message, title=title)





@receiver(post_save, sender=VideoPost)
def create_video_post_notification(sender, instance, created, **kwargs):
    """
    Create notifications for new VideoPost uploads.
    """
    if created:  # Trigger only on creation
        title = "New Reel Uploaded"
        message = f"A new reel titled '{instance.title}' has been added."

        # Fetch all users
        all_users = User.objects.all()

        # Create notifications for all users
        for user in all_users:
            Notification.objects.create(user=user, title=title, message=message)
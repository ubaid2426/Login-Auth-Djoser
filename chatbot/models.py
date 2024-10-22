from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    """
    Model to represent a message between users, with support for text, images, and videos.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    video = models.FileField(upload_to='chat_videos/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.text[:20]}'

    def save(self, *args, **kwargs):
        """
        Customize save behavior to ensure messages from non-admin users go to the admin.
        """
        if not self.sender.is_staff:
            # If the sender is not staff, assign the message to an available admin
            admin_user = User.objects.filter(is_admin=True).first()
            if admin_user:
                self.receiver = admin_user
            else:
                raise ValueError("No admin available to receive messages.")
        super().save(*args, **kwargs)

    @classmethod
    def get_conversation(cls, user):
        """
        Retrieve the conversation between the user (donor) and the admin.
        """
        admin_user = User.objects.filter(is_admin=True).first()
        if not admin_user:
            raise ValueError("No admin available to retrieve messages.")
        
        return cls.objects.filter(
            models.Q(sender=user, receiver=admin_user) |
            models.Q(sender=admin_user, receiver=user)
        ).order_by('timestamp')

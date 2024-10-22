# from django.contrib import admin
# from django.utils.html import format_html
# from .models import Message

# # Register your models here.

# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('sender', 'receiver', 'text', 'timestamp', 'image_preview')
    
#     def image_preview(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" style="width: 45px; height:45px;" />', obj.image.url)
#         return "No Image"
    
#     image_preview.short_description = 'Image Preview'

# # Check if Message is already registered to avoid AlreadyRegistered error
# if not admin.site.is_registered(Message):
#     admin.site.register(Message, MessageAdmin)


from django.contrib import admin
from .models import Message
from django.utils.html import format_html

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'text', 'timestamp', 'image_preview', 'video_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px;" />', obj.image.url)
        return "No Image"
    
    def video_preview(self, obj):
        if obj.video:
            return format_html('<a href="{}" target="_blank">View Video</a>', obj.video.url)
        return "No Video"
    def get_queryset(self, request):
        # Ensure the queryset returns all messages
        qs = super().get_queryset(request)
        return qs
    image_preview.short_description = 'Image Preview'
    video_preview.short_description = 'Video Preview'

admin.site.register(Message, MessageAdmin)

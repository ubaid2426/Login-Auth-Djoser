from django.contrib import admin
from .models import BloodRequest, BottomNavigationItem, DonationImage, IndividualDonorRequest, IndividualCategory, Item, Notification, StaticCategory, VideoPost, CategorySelect, DonationHistory, AllCategoryModel, Category, DonationModel, WorkingHours, DonationRequest
from django.utils.html import format_html



# class DonationOptionsCategoryAdmin(admin.ModelAdmin):
#     list_display = ('title', 'price', 'category', 'category_select')
#     search_fields = ('title', 'category__name', 'category_select__name')

# admin.site.register(DonationOptionsCategory, DonationOptionsCategoryAdmin)
# Register BottomNavigationItem with Admin
@admin.register(BottomNavigationItem)
class BottomNavigationItemAdmin(admin.ModelAdmin):
    list_display = ('disable_icon', 'anable_icon', 'label', 'isSelected')
    list_filter = ('isSelected',)
    search_fields = ('label',)

# Register AllCategoryModel with Admin
@admin.register(AllCategoryModel)
class AllCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_id', 'title', 'route', 'image')
    search_fields = ('title', 'route')
    readonly_fields = ('id',)
    ordering = ('category_id',)
class DonationImageInline(admin.TabularInline):  
    """Allow adding multiple images within a donation"""
    model = DonationImage
    extra = 1  # Shows an empty form to add more images
# @admin.register(DonationImage)
class DonationImageAdmin(admin.ModelAdmin):
    list_display = ("donation", "image_preview")  # Show images in admin panel
    
    def image_preview(self, obj):
        """Show image preview in admin panel."""
        if obj.images:
            return format_html(f"<img src='{obj.images.url}' width='100', />")
            # return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "(No Image)"
    
    image_preview.allow_tags = True  # Allow HTML rendering in admin
    image_preview.short_description = "Preview"
@admin.register(StaticCategory)
class StaticCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_id', 'title', 'route', 'image')
    search_fields = ('title', 'route')
    readonly_fields = ('id',)
    ordering = ('category_id',)


admin.site.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'message', 'email', 'created_at', 'is_read']
@admin.register(IndividualCategory)
class IndividualCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_id', 'title', 'route', 'image')
    search_fields = ('title', 'route')
    readonly_fields = ('id',)
    ordering = ('category_id',)


    # list_filter = ('category_id')
admin.site.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'text1', 'text2', 'detail']
@admin.register(VideoPost)
class VideoPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
@admin.register(CategorySelect)
class CategorySelectAdmin(admin.ModelAdmin):
    list_display = ['title']

# @admin.register(DonationOption)
# class DonationOptionAdmin(admin.ModelAdmin):
#     list_display = ['title', 'price']

# Register DonationModel with Admin
@admin.register(DonationModel)
class DonationModelAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'title', 'project_value', 'paid_value', 'remaining_value', 'category', 'category_select', 'date', 'position')
    list_filter = ('date', 'position')
    search_fields = ('title', 'description')
    readonly_fields = ('remaining_value',)
    ordering = ('-date',)
    inlines = [DonationImageInline] 

# Register WorkingHours with Admin
@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('title', 'days', 'friday')
    search_fields = ('title',)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount_required', 'is_zakat', 'is_sadqah', 'created_at')
    list_filter = ('is_zakat', 'is_sadqah', 'country', 'created_at')
    search_fields = ('name', 'phone', 'city', 'country')

admin.site.register(DonationRequest, DonationRequestAdmin)



@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ('donation',  'donor_name', 'donor_id', 'email', 'amount', 'is_zakat', 'is_sadqah', 'date', 'payment_status', 'Payment_image', 'pay_view', 'image_view', 'heading_category', 'select_category', 'age', 'gender')
    list_filter = ('payment_status', 'date', 'email',)
    list_editable = ('payment_status',)  # Make payment_status editable in the list view
    search_fields = ('donor_name', 'donation__title')
    actions = ['mark_as_completed', 'mark_as_pending']
    def image_view(self, obj):
        if obj.image:
           return format_html(f"<img src='{obj.image.url}' width='100', />")
        return "image not available"
    def pay_view(self, obj):
        if obj.Payment_image:
            return format_html(f"<img src='{obj.Payment_image.url}' width='100', />")
        return "image not available"
    @admin.action(description='Mark selected donations as Completed')
    def mark_as_completed(self, request, queryset):
        queryset.update(payment_status='Completed')

    @admin.action(description='Mark selected donations as Pending')
    def mark_as_pending(self, request, queryset):
        queryset.update(payment_status='Pending')




@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact_number', 'blood_type', 'distance_km', 'time_required', 'quantity', 'created_at']
    search_fields = ['name', 'blood_type']
    list_filter = ['blood_type', 'created_at']        




@admin.register(IndividualDonorRequest)
class IndividualDonorRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'current_location', 'donation_type', 'amount']
    search_fields = ['name', 'contact_number', 'donation_type']
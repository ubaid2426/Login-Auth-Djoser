from django.contrib import admin
from .models import BottomNavigationItem, DonationHistory, AllCategoryModel, Category, DonationModel, WorkingHours, DonationOption, DonationRequest

# Register BottomNavigationItem with Admin
@admin.register(BottomNavigationItem)
class BottomNavigationItemAdmin(admin.ModelAdmin):
    list_display = ('disable_icon', 'anable_icon', 'label', 'isSelected')
    list_filter = ('isSelected',)
    search_fields = ('label',)

# Register AllCategoryModel with Admin
@admin.register(AllCategoryModel)
class AllCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'route', 'image')
    search_fields = ('title', 'route')
    readonly_fields = ('id',)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(DonationOption)
class DonationOptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']

# Register DonationModel with Admin
@admin.register(DonationModel)
class DonationModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_value', 'paid_value', 'remaining_value', 'category', 'date', 'position')
    list_filter = ('date', 'position')
    search_fields = ('title', 'description')
    readonly_fields = ('remaining_value',)
    ordering = ('-date',)

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
    list_display = ('donation', 'donor_name', 'donor_id', 'amount', 'is_zakat', 'is_sadqah', 'date', 'payment_status', 'Payment_image', 'image')
    list_filter = ('payment_status', 'date')
    list_editable = ('payment_status',)  # Make payment_status editable in the list view
    search_fields = ('donor_name', 'donation__title')
    actions = ['mark_as_completed', 'mark_as_pending']

    @admin.action(description='Mark selected donations as Completed')
    def mark_as_completed(self, request, queryset):
        queryset.update(payment_status='Completed')

    @admin.action(description='Mark selected donations as Pending')
    def mark_as_pending(self, request, queryset):
        queryset.update(payment_status='Pending')
from django.contrib import admin
from .models import BottomNavigationItem, AllCategoryModel, Category, DonationModel, WorkingHours, DonationOption

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


from django.db import models
import uuid
# Create your models here.

class BottomNavigationItem(models.Model):
    # Example of storing an icon's name or URL
    disable_icon = models.CharField(max_length=255, blank=True, null=True)  # for storing the icon's name or URL
    anable_icon = models.CharField(max_length=255, blank=True, null=True)  # for storing the icon's name or URL
    label = models.CharField(max_length=255)  # for storing the icon's name or URL
    isSelected = models.BooleanField(default=False)  # boolean field

    def __str__(self):
        return f"Active: {self.is_active}"

    def __str__(self):
        return self.disable_icon if self.disable_icon else "No Icon"



class AllCategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID for unique ID
    title = models.CharField(max_length=255)  # Title of the category
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Image field for storing category images
    route = models.CharField(max_length=255)  # Route field for storing category routes

    def __str__(self):
        return self.title  # Return the title as the string representation


class Category(models.Model):
    title = models.CharField(max_length=255)  # Title of the category

    def __str__(self):
        return self.title  # Return the title as the string representation


def get_default_category():
    return Category.objects.get_or_create(title="Uncategorized")[0].id




class DonationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Image field for storing category images
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='donations', default=get_default_category)
    title = models.CharField(max_length=255)  # Title of the donation project
    description = models.TextField()  # Description of the donation project
    project_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total project value with default
    paid_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Paid amount with default

    date = models.DateField()  # Date of the donation/project
    position = models.IntegerField()  # Position to maintain order
    @property
    def remaining_value(self):
        """Calculate remaining value of the donation project."""
        return self.project_value - self.paid_value

    def __str__(self):
        return f"{self.title} - {self.remaining_value} remaining"












class WorkingHours(models.Model):
    title = models.CharField(max_length=255)
    days = models.TextField()  # Use TextField for potentially longer descriptions
    friday = models.TextField()  # Use TextField for potentially longer descriptions

    def __str__(self):
        return self.title
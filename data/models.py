from django.db import models
from django.utils import timezone
from django.db import models
import uuid
from decimal import Decimal
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
    category_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)  # Title of the category
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Image field for storing category images
    route = models.CharField(max_length=255)  # Route field for storing category routes
    def __str__(self):
        return self.title  # Return the title as the string representation

class DonationOption(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} - ${self.price}"
    



class Category(models.Model):
    title = models.CharField(max_length=255)  # Title of the category

    def __str__(self):
        return self.title  # Return the title as the string representation
class CategorySelect(models.Model):
    title = models.CharField(max_length=255)  # Title of the category

    def __str__(self):
        return self.title  # Return the title as the string representation



def get_default_category():
    return Category.objects.get_or_create(title="Uncategorized")[0].id



class DonationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Image field for storing category images
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='donations', default=get_default_category)
    category_select = models.ForeignKey(CategorySelect, on_delete=models.CASCADE, related_name='donationsselect', default=get_default_category)
    title = models.CharField(max_length=255)  # Title of the donation project
    description = models.TextField()  # Description of the donation project
    project_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total project value with default
    paid_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Paid amount with default
    # donation_options = models.ManyToManyField(DonationOption, blank=True, related_name='donation_projects')
    date = models.DateField()  # Date of the donation/project
    position = models.IntegerField()  # Position to maintain order
    @property
    def remaining_value(self):
        """Calculate remaining value of the donation project."""
        return self.project_value - self.paid_value
    def update_paid_value(self, amount):
        amount = Decimal(amount)
        self.paid_value = amount + self.paid_value
        self.save()

    def __str__(self):
        return f"{self.title} - {self.remaining_value} remaining"





# class Donation1Model(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
#     image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Image field for storing category images
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='donations', default=get_default_category)
#     category_select = models.ForeignKey(CategorySelect, on_delete=models.CASCADE, related_name='donationsselect', default=get_default_category)
#     title = models.CharField(max_length=255)  # Title of the donation project
#     description = models.TextField()  # Description of the donation project
#     project_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total project value with default
#     paid_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Paid amount with default
#     # donation_options = models.ManyToManyField(DonationOption, blank=True, related_name='donation_projects')
#     date = models.DateField()  # Date of the donation/project
#     position = models.IntegerField()  # Position to maintain order
#     @property
#     def remaining_value(self):
#         """Calculate remaining value of the donation project."""
#         return self.project_value - self.paid_value
#     def update_paid_value(self, amount):
#         amount = Decimal(amount)
#         self.paid_value = amount + self.paid_value
#         self.save()

#     def __str__(self):
#         return f"{self.title} - {self.remaining_value} remaining"




class DonationHistory(models.Model):
    donation = models.ForeignKey(DonationModel, on_delete=models.CASCADE, related_name='history')
    donor_name = models.CharField(max_length=255)  # You can adjust as per your user model
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone.now)
    donor_id = models.IntegerField(null=True, blank=True)
    Payment_image = models.ImageField(upload_to='payment_images/', null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    is_zakat = models.BooleanField(default=False, verbose_name="Zakat")
    is_sadqah = models.BooleanField(default=False, verbose_name="Sadqah")
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
        default='Pending'
    )

    def update_amount_or_quantity(self, amount=None, quantity=None):
        """
        Updates either amount or quantity based on the frontend input.
        If amount is provided, update amount and adjust quantity accordingly.
        If quantity is provided, update quantity and adjust amount accordingly.
        """
        if amount is not None:
            self.amount = amount
            if self.donation.project_value > 0:  # Prevent division by zero
                self.quantity = int(amount / (self.donation.project_value / self.donation.remaining_value))
        elif quantity is not None:
            self.quantity = quantity
            self.amount = Decimal(quantity) * (self.donation.project_value / self.donation.remaining_value)
        
        self.save()    


class DonationRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    amount_required = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_zakat = models.BooleanField(default=False)
    is_sadqah = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount_required} (Zakat: {self.is_zakat}, Sadqah: {self.is_sadqah})"
    
class WorkingHours(models.Model):
    title = models.CharField(max_length=255)
    days = models.TextField()  # Use TextField for potentially longer descriptions
    friday = models.TextField()  # Use TextField for potentially longer descriptions

    def __str__(self):
        return self.title



class VideoPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField(upload_to='videos/%y')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
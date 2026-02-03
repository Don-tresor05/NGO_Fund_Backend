from django.db import models
import uuid
from django.conf import settings
from cloudinary.models import CloudinaryField

# Create your models here.


class Dornor(models.Model):
    DONOR_TYPES = [
        ('individual', 'Individual'),
        ('CORPORATE', 'Corporate'),
        ('FOUNDATION', 'Foundation'),
        ('GOVERNMENT', 'Government'),
        ('FAITH-BASED', 'Faith-Based Organization'),
        ('OTHER', 'Other'),
    ]

    DONOR_CATEGORIES = [
       ('REGULAR', 'Regular'),
        ('MONTHLY', 'Monthly'),
        ('MAJOR', 'Major'),
        ('LEGACY', 'Legacy'),
        ('CSR_PROGRAM', 'CSR Program'),
        ('DIASPORA', 'Rwandan Diaspora'),
        ('LOCAL_COMMUNITY', 'Community Group'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('PENDING', 'Pending Approval'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    #Bsic Information
    donor_code = models.CharField(max_length=20, unique=True)
    donor_type = models.CharField(max_length=20, choices=DONOR_TYPES)
    category = models.CharField(max_length=20, choices=DONOR_CATEGORIES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    #Contact Information
    organization_name = models.CharField(max_length=255, blank=True)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternative_phone = models.CharField(max_length=20, blank=True)

    #Address Information
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    #Preferences
    preferred_language = models.CharField(max_length=20, choices=[('EN', 'English'), ('FR', 'French'), ('RW', 'Kinyarwanda')], default='EN')

    communication_preferences = models.CharField(max_length=20, choices=[('EMAIL', 'Email'), ('PHONE', 'Phone'), ('MAIL', 'Mail')], default='EMAIL')

    #Tax Information
    tax_id = models.CharField(max_length=50, blank=True)
    tax_exempt_status = models.BooleanField(default=True)


    #Metadata
    source = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    tags = models.CharField(mdefault=list, blank=True)


    #Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True, related_name='donor_created_by')

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['donor_code']),
                   models.Index(fields=['email']),
                   models.Index(fields=['status']),
                   models.Index(fields=['donor_type']),]
        
        def __str__(self):
            return f"{self.donor_code} - {self.contact_person}"

class Donations(models.Model):
    CURRENCY_CHOICES = [
        ('RWF', 'Rwandan Francs'),
        ('USD', 'US Dollars'),
        ('EUR', 'Euros'),
        ('GBP', 'British Pounds'),
    ]

    PAYMENT_METHODS = [
    )  
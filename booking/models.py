import datetime

from django.db import models
from profiles.models import UserProfile, Address

BOOKING_TYPES =(
        ('TEACHING', 'Teaching'),
        ('PERFORMANCE', 'Performance'),
        ('EQUIPMENT', 'Equipment hire'),
    )

class AdminContact(models.Model):
    """
    Details to be used for invoices
    """
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254)
    payment_details = models.JSONField(encoder=None, decoder=None)
    phone_number = models.CharField(default='', max_length=20, null=False, blank=False)

class Booking(models.Model):
    """
    Stores booking information from enquiry stage
    """
    booking_type = models.CharField(max_length=32, choices=BOOKING_TYPES)
    contact_email = models.EmailField(max_length=254)
    contact_name = models.CharField(max_length=50)
    date_submitted = models.DateField(default=datetime.date.today)
    booking_details = models.JSONField(encoder=None, decoder=None)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

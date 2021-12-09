import datetime

from django.db import models
from profiles.models import UserProfile, Address

BOOKING_TYPES =(
    ('TEACHING', 'Teaching'),
    ('PERFORMANCE', 'Performance'),
    ('EQUIPMENT', 'Equipment hire'),
    ('TEACHING AND EQUIPMENT', 'Teaching and Equipment hire'),
)

PERFORMANCE_TYPES =(
    ('REHEARSAL', 'Rehearsal'),
    ('PERFORMANCE', 'Performance')
)

INSTRUMENTS=(
    ('DRUM KIT', 'Drum Kit'),
    ('PERCUSSION', 'Percussion'),
    ('DULCIMER', 'Dulcimer'),
    ('BODHRAN', 'Dulcimer'),
    ('OTHER', 'Other')
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
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    confirmed = models.BooleanField(default=False)


class PerformanceDetails(models.Model):
    """
    Bookings for performances have specific details which separate them from the other booking types
    """
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    performance_type = models.CharField(max_length=32, choices=PERFORMANCE_TYPES)
    session_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    description = models.CharField(max_length=254, blank=True)


class EquipmentHireDetails(models.Model):
    """
    Bookings for equipment hire have specific details
    which separate them from the other booking types
    """
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    pick_up_time = models.DateTimeField(blank=True)
    return_time = models.DateTimeField(blank=True)
    equipment_hired = models.JSONField(encoder=None, decoder=None)
    description = models.CharField(max_length=254, blank=True)

class TeachingDetails(models.Model):
    """
    Bookings for teaching have specific details which separate them from the other booking types
    """
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    day = models.CharField(max_length=32, blank=True)
    time = models.TimeField(blank=True)
    instrument = models.CharField(max_length=32, choices=INSTRUMENTS)
    lesson_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=254, blank=True)

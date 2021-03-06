import datetime
import uuid

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

GENRE=(
    ('WORLD', 'World'),
    ('POP', 'Pop'),
    ('CONTEMPORARY', 'Contemporary'),
    ('ORCHESTRAL', 'Orchestral'),
    ('OTHER', 'Other'),
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
    booking_number = models.CharField(max_length=32, null=False, editable=False)
    booking_type = models.CharField(max_length=32, choices=BOOKING_TYPES)
    contact_email = models.EmailField(max_length=254)
    contact_name = models.CharField(max_length=50)
    booking_name = models.CharField(max_length=50, blank=True,)
    date_submitted = models.DateField(default=datetime.date.today)
    booking_details = models.JSONField(encoder=None, decoder=None)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    confirmed = models.BooleanField(default=False)

    def _generate_booking_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.contact_name + " - " + self.booking_name
class PerformanceDetail(models.Model):
    """
    Bookings for performances have specific details which separate them from the other booking types
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='performance')
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    performance_type = models.CharField(max_length=32, choices=PERFORMANCE_TYPES)
    session_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                      blank=True, null=True)
    description = models.CharField(max_length=254, blank=True)
    start = models.DateTimeField(blank=True, null=True)
    finish = models.DateTimeField(blank=True, null=True)
    concert_dress = models.CharField(max_length=254, blank=True)


class EquipmentHireDetail(models.Model):
    """
    Bookings for equipment hire have specific details
    which separate them from the other booking types
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='equipment_hire')
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    pick_up_time = models.DateTimeField(blank=True, null=True)
    return_time = models.DateTimeField(blank=True, null=True)
    equipment_hired = models.JSONField(encoder=None, decoder=None)
    description = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return str(self.pick_up_time.date()) + " - " + self.booking.booking_name  
class TeachingDetail(models.Model):
    """
    Although date, time and place may change from lesson to lesson the TeachingDetails mode
    describes the accepted details. To show an example of how the TeachingDetails and
    TeachingInstance models relate: changing the date on TeachingDetails will update all upcoming
    lessons in the related TeachingInstances except for lessons that have already been moved from
    the non-standard time.
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='lesson')
    Address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    student_name = models.CharField(max_length=32, blank=True)
    day = models.CharField(max_length=32, blank=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    instrument = models.CharField(max_length=32, choices=INSTRUMENTS)
    lesson_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=254, blank=True)
    payment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.student_name + " - " + self.instrument.lower().capitalize()

class TeachingInstance(models.Model):
    """
    Encapsulates information relevant to individual lessons
    """
    teaching_details = models.ForeignKey(TeachingDetail, on_delete=models.CASCADE)
    start = models.DateTimeField(blank=True, null=True)
    finish = models.DateTimeField(blank=True, null=True)
    lesson_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.teaching_details.student_name + " - " + str(self.start.date())
class Equipment(models.Model):
    """
    List of equipment available for hire
    """
    genre = models.CharField(max_length=32, choices=GENRE)
    daily_hire_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=254)
    equipment_type = models.CharField(max_length=32)

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
    booking_type = models.CharField(max_length=32, choices=BOOKING_TYPES)
    contact_email = models.EmailField(max_length=254)
    contact_name = models.CharField(max_length=50)
    date_submitted = models.DateField(default=datetime.date.today)
    booking_details = models.JSONField(encoder=None, decoder=None)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.contact_name + " " + self.booking_type + " " + str(self.id)
class PerformanceDetails(models.Model):
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


class EquipmentHireDetails(models.Model):
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

class TeachingDetails(models.Model):
    """
    Although date, time and place may change from lesson to lesson the TeachingDetails model
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
        return self.instrument

class TeachingInstances(models.Model):
    """
    Encapsulates information relevant to individual lessons
    """
    teaching_details = models.ForeignKey(TeachingDetails, on_delete=models.CASCADE)
    day = models.CharField(max_length=32, blank=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    lesson_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Equipment(models.Model):
    """
    List of equipment available for hire
    """
    genre = models.CharField(max_length=32, choices=GENRE)
    daily_hire_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=254)
    equipment_type = models.CharField(max_length=32)

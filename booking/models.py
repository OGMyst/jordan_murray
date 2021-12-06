import datetime

from django.db import models
from django.db.models.fields import CharField
class Enquiry(models.Model):
    """
    New bookings are treated as enquiries and won't be saved to a user until it's confirmed
    """
    class Meta:
        verbose_name_plural = 'Enquiries'

    BOOKING_TYPES =(
        ('TEACHING', 'Teaching'),
        ('PERFORMANCE', 'Performance'),
        ('EQUIPMENT', 'Equipment hire'),
    )

    booking_type = models.CharField(max_length=32, null=False, blank=False, choices=BOOKING_TYPES)
    contact_email = models.EmailField(max_length=254)
    contact_name = models.CharField(max_length=50, null=False, blank=False)
    date_submitted = models.DateField(default=datetime.date.today)
    booking_details = models.JSONField(encoder=None, decoder=None)

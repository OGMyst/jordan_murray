from django.db import models
from django.db.models.fields import CharField
class Enquiry(models.Model):
    BOOKING_TYPES =(
        ('TEACHING', 'Teaching'),
        ('PERFORMANCE', 'Performance'),
        ('EQUIPMENT', 'Equipment hire'),
    )

    BUDGET_RANGES=(
        ('100-200', '100-200'),
        ('200-300', '200-300'),
        ('300-400', '300-400'),
        ('400+', '400+'),
    )
    booking_type = models.CharField(max_length=32, null=False, blank=False, choices=BOOKING_TYPES)
    email = models.EmailField(max_length=254)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    dates = models.JSONField(encoder=None, decoder=None)
    times = models.TimeField(auto_now=False, auto_now_add=False,)
    location = CharField(max_length=50, null=False, blank=False)
    budget = models.CharField(max_length=32, null=False, blank=False, choices=BUDGET_RANGES)
    equipment = models.JSONField(encoder=None, decoder=None)
    description = models.CharField(max_length=1024, null=False, blank=False)

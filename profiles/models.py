from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
class UserProfile(models.Model):
    """
    A user profile model to manage bookings and make payments
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(default='', max_length=50, null=False, blank=False)
    email = models.EmailField(default='', max_length=254, null=False, blank=False)
    phone_number = models.CharField(default='', max_length=20, null=False, blank=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        """
        Create or update the user profile
        """
        if created:
            UserProfile.objects.create(user=instance)
        # Existing users: just save the profile
        instance.userprofile.save()

class Address(models.Model):
    """
    Stores addresses for the many potential venue addresses per user
    """
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80)
    street_address3 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=20)
    country = CountryField(blank_label="Country *", default='GB')
            
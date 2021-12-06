from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    A user profile model to manage bookings and make payments
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    full_name = models.CharField(
        default='', max_length=50, null=False, blank=False)
    email = models.EmailField(
        default='', max_length=254, null=False, blank=False)
    phone_number = models.CharField(
        default='', max_length=20, null=False, blank=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(self, sender, instance, created, **kwargs):
        """
        Create or update the user profile
        """
        if created:
            UserProfile.objects.create(user=instance)
        # Existing users: just save the profile
        instance.userprofile.save()

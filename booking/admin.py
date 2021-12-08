from django.contrib import admin
from .models import Booking, AdminContact

admin.site.register([Booking, AdminContact])

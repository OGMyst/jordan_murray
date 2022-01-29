from django.contrib import admin
from .models import Booking, AdminContact, PerformanceDetails, EquipmentHireDetails, TeachingDetails
class TeachingDetailsAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'Address',
        'day',
        'time',
        'instrument',
        'lesson_cost',
        'description',
    )

admin.site.register([Booking, AdminContact, PerformanceDetails, EquipmentHireDetails])

admin.site.register(TeachingDetails, TeachingDetailsAdmin)

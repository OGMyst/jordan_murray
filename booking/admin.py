from django.contrib import admin
from .models import Booking, AdminContact, PerformanceDetails, EquipmentHireDetails, TeachingDetails, TeachingInstances
class TeachingDetailsAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'Address',
        'day',
        'time',
        'duration',
        'student_name',
        'instrument',
        'lesson_cost',
        'description',
    )

admin.site.register([
    Booking, AdminContact, PerformanceDetails, EquipmentHireDetails,
    TeachingInstances
    ])

admin.site.register(TeachingDetails, TeachingDetailsAdmin)

from django.contrib import admin
from .models import Booking, AdminContact, PerformanceDetails, EquipmentHireDetails, TeachingDetails, TeachingInstance
class TeachingDetailsAdmin(admin.ModelAdmin):
    """
    Stop bothering me
    """
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
    TeachingInstance
    ])

admin.site.register(TeachingDetails, TeachingDetailsAdmin)

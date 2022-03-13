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
class PerformanceDetailsAdmin(admin.ModelAdmin):
    """
    Stop bothering me
    """
    list_display = (
        'booking',
        'Address',
        'performance_type',
        'session_cost',
        'description',
        'start',
        'finish',
        'concert_dress',
    )
    ordering = ('start',)

admin.site.register([
    Booking, AdminContact, EquipmentHireDetails,
    TeachingInstance
    ])

admin.site.register(TeachingDetails, TeachingDetailsAdmin)
admin.site.register(PerformanceDetails, PerformanceDetailsAdmin)

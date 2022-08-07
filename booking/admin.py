from django.contrib import admin
from .models import Booking, AdminContact, PerformanceDetail, Request
from .models import EquipmentHireDetail, TeachingDetail, TeachingInstance


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
class PerformanceDetailAdmin(admin.ModelAdmin):
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
    Booking, AdminContact, EquipmentHireDetail,
    TeachingInstance, Request
    ])

admin.site.register(TeachingDetail, TeachingDetailsAdmin)
admin.site.register(PerformanceDetail, PerformanceDetailAdmin)

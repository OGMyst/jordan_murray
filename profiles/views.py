from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, ContextMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from booking.models import PerformanceDetail, TeachingDetail, EquipmentHireDetail, TeachingInstance
from booking.models import Booking
from .models import UserProfile
from django.contrib.auth.mixins import UserPassesTestMixin

# Used to get relevant information for the selected page
page_objects = {
    "teaching": {
        "b_type": "TEACHING",
        "model": TeachingDetail,
        "include": "includes/teaching.html",
        'order': 'id'
    },

    "performance": {
        "b_type": "PERFORMANCE",
        "model": PerformanceDetail,
        "include": "includes/performance.html",
        'order': 'start'
    },

    "equipment": {
        "b_type": "EQUIPMENT",
        "model": EquipmentHireDetail,
        "include": "includes/equipment.html",
        'order': 'pick_up_time'
    },
}

class ProfileContextMixin(ContextMixin): # pylint: disable=too-few-public-methods
    """
    gets bookings by type and filtered by user.
    if user is a superuser then all bookings of selected type are returned
    """
    @staticmethod
    def booking_information(section, all_bookings, context):

        """
        gets booking by type
        """
        booking_ids = all_bookings.values("id")

        # Selects relevant booking details model and filters results based on IDs
        booking_details = (page_objects[section]["model"]).objects.filter(
            booking__in=booking_ids
        ).order_by(page_objects[section]["order"])

        #performance bookings have their instances combined when viewed on frontend
        overview_details = {}
        calendar_details = {}

        # ------------------------------ LESSON INSTANCES --------------------------------
        if section == 'teaching':

            detail_ids = booking_details.values("id")
            lessons = TeachingInstance.objects.filter(teaching_details__in=detail_ids)
            for lesson in lessons:
                calendar_details[lesson.id] = {
                    'date': f'{lesson.start:%A %d %B}',
                    'student_name': lesson.teaching_details.student_name,
                    'time': f'{lesson.start:%H:%M} - {lesson.finish:%H:%M}',
                    'instrument': lesson.teaching_details.instrument,
                }
                overview_details = booking_details


        # ------------------------------ PERFORMANCE SELECTED --------------------------------

        if section == 'performance':

            for booking in all_bookings:
                overview_details[booking.id] = {
                    'dates_and_times': {
                        'rehearsal': {
                            'dropdown': 0,
                            'slots':{
                            }
                        },
                        'performance': {
                            'dropdown': 0,
                            'slots':{
                            }
                        }
                    }
                }

            #Using booking ID to find the relevant place in the dict -> Add booking details
            for detail in booking_details:

                d_inst = overview_details[detail.booking.id]
                d_inst.update({
                    'booking_name': detail.booking.booking_name,
                    'cost': detail.booking.cost,
                    'concert_dress': detail.concert_dress,
                    'description': detail.description,
                })
                detail_date = f'{detail.start.date():%d/%m/%y}'
                detail_start = f'{detail.start.time():%H:%M}'
                detail_finish = f'{detail.finish.time():%H:%M}'
                slot = f'{detail_start} - {detail_finish} | {detail_date}'

                # So dates can be grouped by performance type more easily on frontend
                d_inst['dates_and_times'][detail.performance_type.lower()]['slots'][slot] = slot
                d_inst['dates_and_times'][detail.performance_type.lower()]['dropdown'] += 1

                calendar_details[detail.id] = {
                    'booking_name': detail.booking.booking_name,
                    'date': f'{detail.start.date():%A %d %B}',
                    'time': f'{detail.start.time():%H:%M} - {detail.finish.time():%H:%M}',
                    'performance_type': detail.performance_type,
                }

        # ------------------------------ EQUIPMENT SELECTED --------------------------------
        if section == 'equipment':

            for equipment in booking_details:
                hiring_dates = f'{equipment.pick_up_time.date()} - {equipment.return_time.date()}'
                numb_of_days = (equipment.return_time.date() - equipment.pick_up_time.date()).days

                overview_details[equipment.booking.id] = {
                    'booking_name': equipment.booking.booking_name,
                    'cost': equipment.booking.cost,
                    'hiring_dates': hiring_dates,
                    'numb_of_days': numb_of_days,
                    'pick_up_time': equipment.pick_up_time.time(),
                    'return_time': equipment.return_time.time(),
                    'date': f'{equipment.pick_up_time.date():%A %d %B}'
                }

                calendar_details = overview_details

        context.update({
            'booking_details': overview_details,
            'include': page_objects[section]["include"],
            'calendar_details': calendar_details

        })
        return context

@method_decorator(login_required, name='dispatch')
class ProfilePageView(TemplateView, ProfileContextMixin):
    """
    For all users except superusers
    """

    template_name = "profile/profile.html"

    def get_context_data(self, section, **kwargs):
        """
        Calls mixin to fetch the correct data by passing the bookings available
        to the user and the selected booking type
        """
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        all_bookings = profile.bookings.filter(
            booking_type=page_objects[section]["b_type"]
        )
        context = (self.booking_information(section, all_bookings, context))
        return context

class ProfileAdminPageView(UserPassesTestMixin, TemplateView, ProfileContextMixin):
    """
    View for superuser to manage all bookings
    """
    template_name = "profile/profile.html"

    def test_func(self):
        """
        User must be a superuser to access all bookings
        """
        return self.request.user.is_superuser

    def get_context_data(self, section, **kwargs):
        """
        Calls mixin to fetch all bookings filtered by selected booking type
        """
        if not section:
            section = 'teaching'

        context = super().get_context_data(**kwargs)
        all_bookings = Booking.objects.all()
        context = (self.booking_information(section, all_bookings, context))
        return context

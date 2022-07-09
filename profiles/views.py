from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic.base import TemplateView, ContextMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from booking.models import PerformanceDetail, TeachingDetail, EquipmentHireDetail, TeachingInstance
from booking.models import Booking
from booking.forms import UpdateTeachingForm
from .models import UserProfile


# Used to differentiate between booking type models 
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

class ProfileContextMixin(ContextMixin):
    """
    Processes Querysets for Booking models to put
    them into more usuable formats on the frontend
    """
    @staticmethod
    def teaching_sort_cal(detail, counter):
        """
        sort data for teaching model data
        """
        lesson = TeachingInstance.objects.filter(teaching_details=detail.id).first()
        if lesson:
            instrument = lesson.teaching_details.instrument.lower().title()

            title = f'{lesson.teaching_details.student_name} - {instrument}'
            calendar_object = {
                counter: {
                    'date': f'{lesson.start:%A %d %B}',
                    'title': title,
                    'extras':{
                        'time': f'{lesson.start:%H:%M} - {lesson.finish:%H:%M}',
                    }
                }
            }
        else:
            calendar_object = {}
        return calendar_object

    @staticmethod
    def performance_sort_cal(detail, counter):
        """
        sort data for perfomance model data
        """
        title = f'{detail.booking.booking_name} - {detail.performance_type.lower().title()}'
        calendar_object = {
            counter: {
                'title': title,
                'date': f'{detail.start.date():%A %d %B}',
                'extras':{
                    'time': f'{detail.start.time():%H:%M} - {detail.finish.time():%H:%M}',
                }
            }
        }

        return calendar_object

    @staticmethod
    def equipment_sort_cal(equipment, counter):
        """
        sort data for equipment model data
        """

        # hiring_dates = f'{equipment.pick_up_time.date()} - {equipment.return_time.date()}'
        # numb_of_days = (equipment.return_time.date() - equipment.pick_up_time.date()).days

        calendar_object = {
            counter: {
                'title': equipment.booking.booking_name,
                'date': f'{equipment.pick_up_time.date():%A %d %B}',
                'extras':{
                    'pick_up_time': f'Pick up: {equipment.pick_up_time.time()}',
                    'return_time': f'Return: {equipment.return_time.time()}',
                },
                # 'cost': equipment.booking.cost,
                # 'hiring_dates': hiring_dates,
                # 'numb_of_days': numb_of_days,
            }
        }

        return calendar_object

    @staticmethod
    def equipment_sort_ovrvw(detail, overview):
        """
        sort data for equipment model data
        """
        hiring_dates = f'{detail.pick_up_time.date()} - {detail.return_time.date()}'
        numb_of_days = (detail.return_time.date() - detail.pick_up_time.date()).days

        overview['equipment'][detail.id] = {
            'booking_name': detail.booking.booking_name,
            'cost': detail.booking.cost,
            'hiring_dates': hiring_dates,
            'numb_of_days': numb_of_days,
            'pick_up_time': detail.pick_up_time.time(),
            'return_time': detail.return_time.time(),
            'date': f'{detail.pick_up_time.date():%A %d %B}',
            'booking_number': detail.booking.booking_number,
        }

        return overview

    @staticmethod
    def teaching_sort_ovrvw(detail, overview):
        """
        sort data for teaching model data
        """

        overview['teaching'][detail.id] = detail
        return overview

    @staticmethod
    def performance_sort_ovrvw(detail,overview):
        """
        sort data for perfomance model data
        """

        perf_book = overview['performance'][detail.booking.id]
        perf_book.update({
            'booking_name': detail.booking.booking_name,
            'cost': detail.booking.cost,
            'concert_dress': detail.concert_dress,
            'description': detail.description,
            'booking_number': detail.booking.booking_number,
        })
        detail_date = f'{detail.start.date():%d/%m/%y}'
        detail_start = f'{detail.start.time():%H:%M}'
        detail_finish = f'{detail.finish.time():%H:%M}'
        slot = f'{detail_start} - {detail_finish} | {detail_date}'

        # So peformance bookings with multiple dates can be grouped more easily on frontend
        perf_book['dates_and_times'][detail.performance_type.lower()]['slots'][slot] = slot
        perf_book['dates_and_times'][detail.performance_type.lower()]['dropdown'] += 1

        return overview


    def sort_calendar(self, all_bookings) -> dict:

        """
        @param p2: Queryset of all selected bookings

        # Get booking type
        # Get related booking details entry
        # Call relevant method to process booking for calendar
        # Add returned object to calendar object
        """

        sorting_funcs = {
            'teaching': self.teaching_sort_cal,
            'performance': self.performance_sort_cal,
            'equipment': self.equipment_sort_cal,

        }
        counter = 0
        calendar = {}
        # for each item in the booking model
        for booking_inst in all_bookings:
            type_lowered = booking_inst.booking_type.lower()
            sort_func = sorting_funcs[type_lowered]
            #get the related details model to that booking
            booking_details = (page_objects[type_lowered]["model"]).objects.filter(
                booking=booking_inst.id
            )

            for detail in booking_details:
                calendar_object = sort_func(detail, counter)
                counter += 1
                calendar.update(calendar_object)
        return calendar


    def sort_overview(self, all_data) -> dict:

        """
        @param p2: [Queryset of all selected bookings, Dict of booking types]

        # Get booking type
        # Get related booking details entry
        # Call relevant method to process booking for Overview
        # Add returned object to Overview object
        """

        all_bookings = all_data[0]
        overview = all_data[1]

        sorting_funcs = {
            'teaching': self.teaching_sort_ovrvw,
            'performance': self.performance_sort_ovrvw,
            'equipment': self.equipment_sort_ovrvw,
        }

        # for each item in the booking model
        for booking_inst in all_bookings:
            type_lowered = booking_inst.booking_type.lower()
            sort_func = sorting_funcs[type_lowered]
            #get the related details model to that booking
            booking_details = (page_objects[type_lowered]["model"]).objects.filter(
                booking=booking_inst.id
            )
            for detail in booking_details:
                overview_object = sort_func(detail, overview)
                overview.update(overview_object)
        return overview

@method_decorator(login_required, name='dispatch')
class ProfilePageView(TemplateView, ProfileContextMixin):
    """
    For all users except superusers
    """

    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        """
        Calls mixin to fetch the correct data by passing the bookings available
        to the user and the selected booking type
        """

        context = super().get_context_data(**kwargs)
        booking_types = {
            'teaching': {},
            'performance': {},
            'equipment': {},
        }

        if self.request.user.is_superuser:

            all_bookings = Booking.objects.all()
            context.update({
                'second_menu': 'includes/admin_menu.html',
            })
        else:
            profile = get_object_or_404(UserProfile, user=self.request.user)
            all_bookings = profile.bookings.all()
            context.update({
                'second_menu': 'includes/standard_menu.html',
            })

        for booking in all_bookings:
            if booking.booking_type.lower() == 'performance':
                booking_types['performance'].update({
                    booking.id:{
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
                })

        overview_details = self.sort_overview([all_bookings, booking_types])
        calendar_details = self.sort_calendar(all_bookings)

        context.update({
            'booking_details': overview_details,
            'calendar_details': calendar_details
        })

        return context

class UpdateBookingView(TemplateView, ProfileContextMixin):
    """
    lala
    """
    form_class = UpdateTeachingForm
    template_name = "profile/update_booking.html"

    def get_context_data(self, **kwargs):
        """
        Calls mixin to fetch the correct data by passing the bookings available
        to the user and the selected booking type
        """

        context = super().get_context_data(**kwargs)

        booking_number = context['booking_number']
        selected_booking = Booking.objects.filter(
                booking_number=booking_number
        )
        # Although only one booking is being processed, this dict allows for the same method to
        # be called as used for the profile booking page
        booking_types = {
            'teaching': {},
            'performance': {},
            'equipment': {},
        }

        overview_details: dict = self.sort_overview([selected_booking, booking_types])
        booking_instance = ''

        #Pulls the booking from dict, removing uneeded multibooking structure
        for key, value in overview_details.items():
            if value:
                get_key_value_pair = list(value.items())[0]
                booking_instance = get_key_value_pair[1]
                break

        booking_type = booking_instance.booking.booking_type.lower()

        initial_form_values: dict = self.update_teaching_form(selected_booking)
        form = UpdateTeachingForm(initial=initial_form_values)

        context.update({
                'booking': booking_instance,
                'second_menu': 'includes/admin_menu.html',
                'booking_type': f'includes/booking-updates/{booking_type}.html',
                'form': form
            })
        return context

    def update_teaching_form(self, selected_booking) -> dict:
        """
        @param p1: Queryset of booking selected to be updated

        # Get related Detail Model for booking
        # Go through each field in the modelForm and pull a value from the Detail model
        # Return dict to pre-populate the modelForm with the current values
        """
        booking_detail = TeachingDetail.objects.filter(
                booking=selected_booking[0].id
        ).values()

        populated_fields = {}
        transformed_queryset = booking_detail[0]

        for field in UpdateTeachingForm().fields:
            populated_fields[field] = transformed_queryset[field]
        return populated_fields

    def post(self, request, booking_number):
        """
        lala
        """
        related_booking = Booking.objects.get(booking_number=booking_number)
        booking_type_model = page_objects[related_booking.booking_type.lower()]['model']
        teaching = get_object_or_404(booking_type_model, booking=related_booking.id)
        form = UpdateTeachingForm(request.POST, instance=teaching)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))

        return render(request, self.template_name, {'form':form})
    
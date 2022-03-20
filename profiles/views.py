from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from booking.models import PerformanceDetail, TeachingDetail, EquipmentHireDetail, TeachingInstance
from .models import UserProfile

@method_decorator(login_required, name='dispatch')
class ProfilePageView(TemplateView):
    """
    profile thing
    """

    template_name = "profile/profile.html"

    def get_context_data(self, section, **kwargs):
        """
        Gets relevant data and which include template to use for profile page
        """
        context = super().get_context_data(**kwargs)

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
        profile = get_object_or_404(UserProfile, user=self.request.user)

        # Gets booking instances for selected booking type
        all_bookings = profile.bookings.filter(
            booking_type=page_objects[section]["b_type"]
        )
        booking_ids = all_bookings.values("id")

        # Selects relevant booking details model and filters results based on IDs
        booking_details = (page_objects[section]["model"]).objects.filter(
            booking__in=booking_ids
        ).order_by(page_objects[section]["order"])

        #performance bookings have their instances combined when viewed on frontend
        overview_details = {}
        calendar_details = {}
        dropdown = {
            'rehearsal': False,
            'concert': False,
        }

        # ------------------------------ LESSON INSTANCES --------------------------------
        if section == 'teaching':

            detail_ids = booking_details.values("id")
            lessons = TeachingInstance.objects.filter(teaching_details__in=detail_ids)
            for lesson in lessons:
                calendar_details[lesson.id] = {}
                l_inst = calendar_details[lesson.id]
                l_inst['date'] = f'{lesson.start:%A %d %B}'
                l_inst['student_name'] = lesson.teaching_details.student_name
                l_inst['time'] = f'{lesson.start:%H:%M} - {lesson.finish:%H:%M}'
                l_inst['instrument'] = lesson.teaching_details.instrument
                overview_details = booking_details


        # ------------------------------ PERFORMANCE SELECTED --------------------------------

        if section == 'performance':
            # To index concert and rehearsal entries into the dict
            r_counter = 0
            c_counter = 0

            # Make an empty dict for each performance booking then insert booking name
            for  b_instance in all_bookings:
                overview_details[b_instance.id] = {}
                perf_inst = overview_details[b_instance.id] #to save on horizontal space
                perf_inst['dates_and_times'] = {}
                perf_inst['dates_and_times']['rehearsal'] = {}
                perf_inst['dates_and_times']['concert'] = {}
                perf_inst['booking_name'] = b_instance.booking_name
                perf_inst['cost'] = b_instance.cost

            #Using booking ID to find the relevant place in the dict -> Add booking details
            for detail in booking_details:
                d_inst = overview_details[detail.booking.id]
                detail_date = f'{detail.start.date():%d/%m/%y}'
                detail_start = f'{detail.start.time():%H:%M}'
                detail_finish = f'{detail.finish.time():%H:%M}'
                slot = f'{detail_start} - {detail_finish} | {detail_date}'

                # So dates can be grouped by performance type more easily on frontend
                if detail.performance_type == 'REHEARSAL':
                    d_inst['dates_and_times']['rehearsal'][r_counter] = slot
                    r_counter += 1
                else:
                    d_inst['dates_and_times']['concert'][c_counter] = slot
                    c_counter += 1
                d_inst['concert_dress'] = detail.concert_dress
                d_inst['description'] = detail.description

            for detail in booking_details:
                calendar_details[detail.id] = {}
                cal_slot = calendar_details[detail.id]
                cal_slot['booking_name'] = detail.booking.booking_name
                cal_slot['date'] = f'{detail.start.date():%A %d %B}'
                cal_slot['time'] = f'{detail.start.time():%H:%M} - {detail.finish.time():%H:%M}'
                cal_slot['performance_type'] = detail.performance_type

            if r_counter:
                dropdown['rehearsal'] = True
            if c_counter > 1:
                dropdown['concert'] = True

        # ------------------------------ EQUIPMENT SELECTED --------------------------------
        if section == 'equipment':

            for equipment in booking_details:
                hiring_dates = f'{equipment.pick_up_time.date()} - {equipment.return_time.date()}'
                numb_of_days = (equipment.return_time.date() - equipment.pick_up_time.date()).days

                overview_details[equipment.booking.id] = {}
                equip_inst = overview_details[equipment.booking.id]
                equip_inst['booking_name'] = equipment.booking.booking_name
                equip_inst['cost'] = equipment.booking.cost
                equip_inst['hiring_dates'] = hiring_dates
                equip_inst['numb_of_days'] = numb_of_days
                equip_inst['pick_up_time'] = equipment.pick_up_time.time()
                equip_inst['return_time'] = equipment.return_time.time()
                equip_inst['date'] = f'{equipment.pick_up_time.date():%A %d %B}'

        context["booking_details"] = overview_details
        if calendar_details:
            context["calendar_details"] = calendar_details
        context["include"] = page_objects[section]["include"]
        context["dropdown"] = dropdown
        return context

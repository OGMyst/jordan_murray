from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from booking.models import PerformanceDetails, TeachingDetails, EquipmentHireDetails, TeachingInstance
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
                "model": TeachingDetails,
                "include": "includes/teaching.html",
            },
            
            "performance": {
                "b_type": "PERFORMANCE",
                "model": PerformanceDetails,
                "include": "includes/performance.html",
            },

            "equipment": {
                "b_type": "EQUIPMENT",
                "model": EquipmentHireDetails,
                "include": "includes/equipment.html",
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
        )

        #performance bookings have their instances combined when viewed on frontend
        perfomances = {}
        calendar_details = {}
        # ------------------------------ LESSON INSTANCES --------------------------------
        if section == 'teaching':

            detail_ids = booking_details.values("id")
            lessons = TeachingInstance.objects.filter(teaching_details__in=detail_ids)
            for lesson in lessons:
                perfomances[lesson.teaching_details_id] = {}
                l_inst = perfomances[lesson.teaching_details_id]
                l_inst['date'] = f'{lesson.start:%A %d %B}'
                l_inst['student_name'] = lesson.teaching_details.student_name
                l_inst['time'] = f'{lesson.start:%H:%M} - {lesson.finish:%H:%M}'
                calendar_details = perfomances
        # ------------------------------ PERFORMANCE SELECTED --------------------------------

        if section == 'performance':
            # To index concert and rehearsal entries into the dict
            r_counter = 0
            c_counter = 0

            # Make an empty dict for each performance booking then insert booking name
            for  b_instance in all_bookings:
                perfomances[b_instance.id] = {}
                perf_inst = perfomances[b_instance.id] #to save on horizontal space
                perf_inst['dates_and_times'] = {}
                perf_inst['dates_and_times']['rehearsal'] = {}
                perf_inst['dates_and_times']['concert'] = {}
                perf_inst['booking_name'] = b_instance.booking_name
                perf_inst['cost'] = b_instance.cost

            #Using booking ID to find the relevant place in the dict -> Add booking details
            for detail in booking_details:
                d_inst = perfomances[detail.booking.id]
                dt_converted = f'{detail.start.date()} {detail.start.time()}-{detail.finish.time()}'

                # So dates can be grouped by performance type more easily on frontend
                if detail.performance_type == 'REHEARSAL':
                    d_inst['dates_and_times']['rehearsal'][r_counter] = dt_converted
                    r_counter += 1
                else:
                    d_inst['dates_and_times']['concert'][c_counter] = dt_converted
                    c_counter += 1
                d_inst['concert_dress'] = detail.concert_dress
                d_inst['description'] = detail.description
            booking_details = perfomances


        # ------------------------------ EQUIPMENT SELECTED --------------------------------
        if section == 'equipment':
            for  equipment in all_bookings:
                perfomances[equipment.id] = {}
                equip_inst = perfomances[equipment.id] #to save on horizontal space
                equip_inst['booking_name'] = equipment.booking_name
                equip_inst['cost'] = equipment.cost

            #Using booking ID to find the relevant place in the dict -> Add booking details
            for detail in booking_details:
                d_inst = perfomances[detail.booking.id]
                hiring_dates = f'{detail.pick_up_time.date()} - {detail.return_time.date()}'
                numb_of_days = (detail.return_time.date() - detail.pick_up_time.date()).days
                pick_up_time = detail.pick_up_time.time()
                return_time = detail.return_time.time()

                d_inst['hiring_dates'] = hiring_dates
                d_inst['numb_of_days'] = numb_of_days
                d_inst['pick_up_time'] = pick_up_time
                d_inst['return_time'] = return_time

            booking_details = perfomances

        context["booking_details"] = booking_details
        if calendar_details:
            context["calendar_details"] = calendar_details

        context["include"] = page_objects[section]["include"]
        return context

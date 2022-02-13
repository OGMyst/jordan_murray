from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from booking.models import PerformanceDetails, TeachingDetails
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
        }
        profile = get_object_or_404(UserProfile, user=self.request.user)
        all_bookings = profile.bookings.filter(
            booking_type=page_objects[section]["b_type"]
        )
        booking_ids = all_bookings.values("id")
        booking_details = (page_objects[section]["model"]).objects.filter(
            booking__in=booking_ids
        )

        #performance bookings have their instances combined when viewed on frontend
        perfomances = {}
        if section == 'performance':
            r_counter = 0
            c_counter = 0

            # Make an empty dict for each performance booking then insert booking name
            for  b_instance in all_bookings:
                perfomances[b_instance.id] = dict()
                perf_inst = perfomances[b_instance.id] #to save on horizontal space
                perf_inst['dates_and_times'] = dict()
                perf_inst['dates_and_times']['rehearsal'] = dict()
                perf_inst['dates_and_times']['concert'] = dict()
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

        context["booking_details"] = booking_details
        context["include"] = page_objects[section]["include"]
        return context

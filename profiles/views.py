from re import template
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from booking.models import PerformanceDetails, TeachingDetails, Booking
from .models import UserProfile

# @login_required
class ProfilePageView(TemplateView):
    """
    profile thing
    """
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        """
        Gets relevant data and include for profile page
        """
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        all_bookings = profile.bookings.filter(booking_type='TEACHING').values('id')
        lessons = TeachingDetails.objects.filter(booking__in=all_bookings)

        context['lessons'] = lessons
        context['include'] = 'includes/teaching.html'
        return context

    # def get_performance(request):
    #     profile = get_object_or_404(UserProfile, user=request.user)

    #     booking = profile.bookings.filter(booking_type='PERFORMANCE').values('id')
    #     gigs = PerformanceDetails.objects.filter(booking__in=booking)

    #     context = {
    #         'gigs': gigs,
    #         'include': 'includes/performance.html',
    #     }
    #     return render('includes/performance.html', context)

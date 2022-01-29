from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from booking.models import TeachingDetails, Booking
from .models import UserProfile

@login_required
def profile(request):
    """ A view to return the profile page """
    profile = get_object_or_404(UserProfile, user=request.user)

    booking = profile.bookings.filter(booking_type='TEACHING').values('id')[0]['id']
    lessons = TeachingDetails.objects.filter(booking=booking)
    print(timedelta(hours=1))
    context = {
        'lessons': lessons
    }
    return render(request, 'profile/profile.html', context)

from django.shortcuts import render
from .forms import BookingForm, TeachingForm


def booking(request):
    """ A view to return the booking page """
    if request.method == 'POST':
        print('HI')
    else:
        booking_form = BookingForm()
        teaching_form = TeachingForm()

    template = 'booking/booking.html'
    context = {
        'booking_form': booking_form,
        'teaching_form': teaching_form,
    }

    return render(request, template, context)

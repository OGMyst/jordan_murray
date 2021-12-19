from django.shortcuts import render, redirect, reverse
from .forms import BookingForm, TeachingForm


def booking(request):
    """ A view to return the booking page """
    booking_form = BookingForm()
    teaching_form = TeachingForm()

    form_lookup = {
        'booking': booking_form,
        'teaching': teaching_form,
    }
    if request.method == 'POST':
        # Decide 2nd step in form by using service
        if 'one' in request.POST:
            service = request.POST['service'].lower()
            context = {
                'form': form_lookup[service],
                'step': 'two',
            }
        if 'two' in request.POST:
            return redirect(reverse('home'))
    else:
        context = {
            'form': booking_form,
            'step': 'one',
        }

    template = 'booking/booking.html'

    return render(request, template, context)

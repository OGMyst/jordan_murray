import json
import copy
from django.shortcuts import render

from booking.models import Booking
from .forms import BookingForm



def booking(request):
    """A view to return the booking page"""

    booking_form = BookingForm()

    # Get values for field which appear across all models. JSONify the rest
    if request.method == 'POST':
        submitted_form = copy.copy(request.POST)

        #Removes empty values from unsused forms
        cleaned_form = {k: v for k, v in submitted_form.items() if v}
        cleaned_form.pop('submit')
        booking_form = BookingForm(request.POST)

        if booking_form.is_valid():
            print('is valid')

            #Remove fields not belonging to the booking details field
            booking_type = cleaned_form['service']
            contact_email = cleaned_form['email']
            contact_name = cleaned_form['name']

            cleaned_form.pop('service')
            cleaned_form.pop('email')
            cleaned_form.pop('name')

            # Service specifc fields are stored in a JSON field
            booking_details = json.dumps(cleaned_form)
            
            booked = Booking(
                booking_type = booking_type,
                contact_email =  contact_email,
                contact_name =  contact_name,
                booking_details = booking_details,
            )
            booked.save()
            template = "booking/thank you.html"
            return render(request, template)
            
        else:
            print (booking_form.errors)
            print('not valid')

    context = {
        "booking_form": booking_form,
    }

    template = "booking/booking.html"

    return render(request, template, context)

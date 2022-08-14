from datetime import datetime
import json
import copy
from django.shortcuts import render

from booking.models import Request
from .forms import RequestForm



def booking(request):
    """A view to return the booking page"""

    request_form = RequestForm()

    # Get values for field which appear across all models. JSONify the rest
    if request.method == 'POST':
        submitted_form = copy.copy(request.POST)

        #Removes empty fields from form.
        #required as form has fields for models other than request
        cleaned_form = {k: v for k, v in submitted_form.items() if v}
        cleaned_form.pop('submit')

        request_form = RequestForm(submitted_form)

        if request_form.is_valid():

            #Remove fields not belonging to the booking details field
            booking_type = cleaned_form['service']
            contact_email = cleaned_form['email']
            contact_name = cleaned_form['name']
            cleaned_form.pop('service')
            cleaned_form.pop('email')
            cleaned_form.pop('name')

            # Service specifc fields are stored in a JSON field
            booking_details = json.dumps(cleaned_form)

            booking_request = Request(
                booking_type = booking_type,
                contact_email =  contact_email,
                contact_name =  contact_name,
                booking_details = booking_details,
            )
            booking_request.save()
            template = "booking/thank you.html"
            return render(request, template)

    context = {
        "request_form": request_form,
    }

    template = "booking/booking.html"

    return render(request, template, context)

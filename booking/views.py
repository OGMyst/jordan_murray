import json
import copy
from django.shortcuts import render

from booking.models import Booking
from .forms import BookingForm



def booking(request):
    """A view to return the booking page"""
    # Users have 3 service to pick from: teaching, performance, equipment hire. Each booking type
    # has slight difference in the information required therefore the submitted form will be
    # different as well.

    # A submitted booking will have the essential details for jordan to review but the service
    # specific information will be contained inside a JSON field until the details are confirmed.

    # Once the details have been confirmed the full booking and related service will be entered
    # with all the information

    # To create the booking instance: Take the submitted information -> Set a new dict with the
    # fields from the booking model -> All service specific information goes inside a JSON object
    # in the "booking_details" field

    # When users land on the page all 4 forms will be rendered but only the booking form will be
    # visible On clicking next users will be shown the next form based on the selected service

    booking_form = BookingForm()

    # When users submit the form the information is extracted and placed into the correct fields
    # This is done manually since each submitted form can be different

    # To validate multiple submitted dates try this code
    # function isValidDate(value) {
    # var dateWrapper = new Date(value);
    # return !isNaN(dateWrapper.getDate());}

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

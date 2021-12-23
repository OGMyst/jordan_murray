from django.shortcuts import render
from .forms import BookingForm
# , TeachingForm, EquipmentForm, PerformanceForm


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
    # teaching_form = TeachingForm()
    # performance_form = PerformanceForm()
    # equipment_form = EquipmentForm()

    # When users submit the form the information is extracted and placed into the correct fields
    # This is done manually since each submitted form can be different

    # To validate multiple submitted dates try this code
    # function isValidDate(value) {
    # var dateWrapper = new Date(value);
    # return !isNaN(dateWrapper.getDate());}
    if request.method == 'POST':
        print(request.POST)
 
    context = {
        "booking_form": booking_form,
        # "teaching_form": teaching_form,
        # "performance_form": performance_form,
        # "equipment_form": equipment_form,
    }

    template = "booking/booking.html"

    return render(request, template, context)

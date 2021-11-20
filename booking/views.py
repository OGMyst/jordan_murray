from django.shortcuts import render

def booking(request):
    """ A view to return the booking page """

    return render(request, 'booking/booking.html')

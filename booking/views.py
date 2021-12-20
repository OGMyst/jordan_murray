from django.shortcuts import render, redirect, reverse
from .forms import BookingForm, TeachingForm


def booking(request):
    """A view to return the booking page"""
    booking_form = BookingForm()
    teaching_form = TeachingForm()

    context = {
        "booking_form": booking_form,
        "ßteaching_form": teaching_form,
    }

    template = "booking/booking.html"

    return render(request, template, context)

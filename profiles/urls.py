from django.urls import path
from .views import ProfilePageView, UpdateBookingView

urlpatterns = [
    path('', ProfilePageView.as_view()),
    path('<booking_number>', UpdateBookingView.as_view())
]

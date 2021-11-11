from django.shortcuts import render


# Create your views here.
from bookingapp.models import Booking


def bookings(request):
    bookings = Booking.objects.all()
    context = {
        "bookings": bookings
    }
    return render(request, "bookings.html", context)

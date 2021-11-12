from django.shortcuts import render
from bookingapp.models import Booking, Room
from .forms import BookForm
from django.db.models import Q


# Create your views here.
def bookings_view(request):
    bookings = Booking.objects.all()
    context = {
        "bookings": bookings
    }
    return render(request, "bookings.html", context)


def book_view(request):
    if request.method == "POST":
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            possible_rooms = Room.objects.filter(
                type__size__gte=book_form.cleaned_data["guests"],
            )

            already_booked = Booking.objects.filter(
                Q(
                    date_from__in=[book_form.cleaned_data["date_from"], book_form.cleaned_data["date_to"]],
                    room__type__size__lte=book_form.cleaned_data["guests"]
                ) |
                Q(
                    date_to__in=[book_form.cleaned_data["date_from"], book_form.cleaned_data["date_to"]],
                    room__type__size__lte=book_form.cleaned_data["guests"]
                  ) |
                Q(
                    date_from__lte=book_form.cleaned_data["date_from"],
                    date_to__gte=book_form.cleaned_data["date_to"],
                    room__type__size__lte=book_form.cleaned_data["guests"]
                  )
            )

            count_possible_rooms = possible_rooms.count()

            booked_rooms = already_booked.count()

            if count_possible_rooms - booked_rooms >= 1:
                res = True
            else:
                res = False

            context = {
                "possible_rooms": possible_rooms,
                "already_booked": already_booked,
                "booked_rooms": booked_rooms,
                "res": res
            }
            return render(request, 'booking_confirm.html', context)
    else:
        book_form = BookForm()

    context = {
        "book_form": book_form
    }
    return render(request, "search.html", context)

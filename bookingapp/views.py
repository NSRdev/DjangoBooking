from time import strftime

from django.contrib import messages
from django.shortcuts import render, redirect
from bookingapp.models import Booking, Room
from .forms import BookForm, ConfirmationForm
from django.db.models import Q
from datetime import datetime


# Create your views here.
def bookings_view(request):
    bookings = Booking.objects.all()
    context = {
        "bookings": bookings
    }
    return render(request, "bookings.html", context)


def details_view(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    context = {
        "booking": booking
    }
    return render(request, "details.html", context)


def delete_view(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()

    messages.info(request, 'Your reservation has been deleted successfully')
    return redirect('/')


def search_view(request):
    book_form = BookForm()
    context = {
        "book_form": book_form
    }
    return render(request, "search.html", context)


def select_view(request):
    if request.method == "POST":
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            date_from = request.session["date_from"] = book_form.cleaned_data["date_from"].strftime("%Y-%m-%d")
            date_to = request.session["date_to"] = book_form.cleaned_data["date_to"].strftime("%Y-%m-%d")
            guests = request.session["guests"] = book_form.cleaned_data["guests"]

            booked_rooms = Booking.objects.filter(
                Q(date_from__range=[date_from, date_to]) |
                Q(date_to__range=[date_from, date_to])
            )

            booked_rooms_id = booked_rooms.values_list('room_id')

            available_rooms = Room.objects.exclude(id__in=booked_rooms_id).filter(
                type__size__gte=guests,
            )

            context = {
                "available_rooms": available_rooms,
                "booked_rooms": booked_rooms,
            }
            return render(request, 'select.html', context)
    else:
        book_form = BookForm()
    context = {
        "book_form": book_form
    }
    return render(request, "search.html", context)


def confirm_view(request):
    if request.method == "POST":
        room_id = request.POST["room_id"]
        room = Room.objects.get(id=room_id)
        date_from = datetime.strptime(request.session["date_from"], "%Y-%m-%d").date()
        date_to = datetime.strptime(request.session["date_to"], "%Y-%m-%d").date()

        duration = date_to - date_from
        request.session["duration"] = duration.days
        request.session["total_price"] = float(duration.days) * float(room.price)
        request.session["room_id"] = room_id

        confirmation_form = ConfirmationForm()
        context = {
            "confirmation_form": confirmation_form,
            "room": room,
        }
        return render(request, "confirm.html", context)


def save_view(request):
    if request.method == "POST":
        confirmation_form = ConfirmationForm(request.POST)

        if confirmation_form.is_valid():
            room_id = request.session["room_id"]
            room = Room.objects.get(id=room_id)

            contact_name = confirmation_form.cleaned_data.get("contact_name")
            contact_email = confirmation_form.cleaned_data.get("contact_email")
            contact_phone = confirmation_form.cleaned_data.get("contact_phone")

            guests = request.session["guests"]
            total_price = request.session["total_price"]
            date_from = datetime.strptime(request.session["date_from"], "%Y-%m-%d").date()
            date_to = datetime.strptime(request.session["date_to"], "%Y-%m-%d").date()

            Booking.objects.create(
                room=room,
                guests=guests,
                date_from=date_from,
                date_to=date_to,
                contact_name=contact_name,
                contact_email=contact_email,
                contact_phone=contact_phone,
                total_price=total_price
            )
            messages.success(request, 'Your reservation has been confirmed successfully')
            return redirect('/')
    else:
        confirmation_form = ConfirmationForm()
    context = {
        "confirmation_form": confirmation_form
    }
    return render(request, 'confirm.html', context)
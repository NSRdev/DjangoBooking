from django.db import models
import uuid


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=20)
    size = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name + " | " + str(self.price) + "€/day"


class Booking(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guests = models.IntegerField()
    date_from = models.DateField()
    date_until = models.DateField()
    contact_name = models.CharField(max_length=40)
    contact_email = models.EmailField(max_length=40)
    contact_phone = models.CharField(max_length=9)
    created = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.room.name + " | " + str(self.date_from) + " // " + str(self.date_until) + " | " + self.contact_name

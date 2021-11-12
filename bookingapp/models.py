from django.db import models
import uuid


# Create your models here.
class RoomType(models.Model):
    name = models.CharField(max_length=20)
    size = models.IntegerField()

    def __str__(self):
        return "Name: " + self.name + " | Size: " + str(self.size)


class Room(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=120)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    number = models.IntegerField()

    def __str__(self):
        return "Name: " + str(self.name) + " | Type: " + self.type.name


class Booking(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guests = models.IntegerField()
    date_from = models.DateField()
    date_to = models.DateField()
    contact_name = models.CharField(max_length=40)
    contact_email = models.EmailField(max_length=40)
    contact_phone = models.CharField(max_length=9)
    created = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.room.name + " | " + str(self.date_from) + " // " + str(self.date_to) + " | " + self.contact_name

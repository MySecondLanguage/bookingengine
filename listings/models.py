from django.db import models
from django.core.exceptions import ValidationError


class Listing(models.Model):
    HOTEL = 'hotel'
    APARTMENT = 'apartment'
    LISTING_TYPE_CHOICES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
    )

    listing_type = models.CharField(
        max_length=16,
        choices=LISTING_TYPE_CHOICES,
        default=APARTMENT
    )
    title = models.CharField(max_length=255,)
    country = models.CharField(max_length=255,)
    city = models.CharField(max_length=255,)

    def __str__(self):
        return self.title
    

class HotelRoomType(models.Model):
    hotel = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_room_types'
    )
    title = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.hotel} - {self.title}'


class HotelRoom(models.Model):
    hotel_room_type = models.ForeignKey(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_rooms'
    )
    room_number = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.room_number} - {self.hotel_room_type}'


class BookingInfo(models.Model):
    listing = models.OneToOneField(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info'
    )
    hotel_room_type = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info',
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        if self.listing:
            obj = self.listing
        else:
            obj = self.hotel_room_type
            
        return f'{obj} {self.price}'



class DaySlot(models.Model):
    room = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="room_day_slots",
    )
    apartment = models.ForeignKey( # store only if listing type aparthment
        Listing,
        on_delete=models.CASCADE,
        related_name="apartment_day_slots",
        null=True,
        blank=True,
    )
    spot = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['spot', 'apartment'], name='apartment_slots'),
            models.UniqueConstraint(fields=['spot', 'room'], name='room_slots'),
        ]

    def clean(self):
        if self.room and self.apartment:
            raise ValidationError("You can't book both room and appartment together")
        
        if self.apartment:
            if self.appartment.listing_type != 'apartment':
                raise ValidationError("The instance is not apartment type")

    def __str__(self):
        return f'{self.spot} - {self.room} - {self.apartment}'
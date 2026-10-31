
from django.db import models
from django.conf import settings


class Room(models.Model):

    ROOM_TYPES = [
        ('SINGLE', 'Single'),
        ('SHARED', 'Shared'),
        ('MASTER', 'Master'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)

    latitude = models.DecimalField(
        max_digits=10, decimal_places=7,
        null=True, blank=True
    )

    longitude = models.DecimalField(
        max_digits=10, decimal_places=7,
        null=True, blank=True
    )

    rent = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES
    )

    available_from = models.DateField()

    amenities = models.ManyToManyField(
        'Amenity',
        related_name='rooms',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_room_details(self):
        return {
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'rent': self.rent,
            'room_type': self.room_type,
        }

    def get_images(self):
        return self.images.all()

    def get_amenities(self):
        return self.amenities.all()

    def get_location(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.location
        }

    def __str__(self):
        return self.title


class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='room_images/')

    is_primary = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def set_primary(self):
        RoomImage.objects.filter(
            room=self.room
        ).update(is_primary=False)

        self.is_primary = True
        self.save(update_fields=['is_primary'])

    def __str__(self):
        return f"Image for {self.room.title}"


class Amenity(models.Model):

    name = models.CharField(max_length=100, unique=True)

    icon = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
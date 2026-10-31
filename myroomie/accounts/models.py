from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        TENANT = "TENANT", "Tenant"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.TENANT
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    university = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    ref_loc = models.CharField(max_length=255, blank=True)
    ref_latitude = models.FloatField(null=True, blank=True)
    ref_longitude = models.FloatField(null=True, blank=True)

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Preference(models.Model):
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="preference"
    )

    location_preference = models.CharField(
        max_length=200, blank=True
    )
    budget_min = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    budget_max = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    gender_preference = models.CharField(
        max_length=30, blank=True
    )
    lifestyle = models.TextField(blank=True)
    preferred_room_type = models.CharField(
        max_length=50, blank=True
    )
    additional_notes = models.TextField(blank=True)

    food_type = models.CharField(max_length=50, blank=True)
    smoking = models.CharField(max_length=20, blank=True)
    sleep_time = models.CharField(max_length=50, blank=True)
    cleanliness = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Preference: {self.user.name}"


class RoommateRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    sender = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="sent_requests"
    )
    receiver = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="received_requests"
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

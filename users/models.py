from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        default="default_profile.jpg",
        blank=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?\d{10,15}$",
                message="Enter a valid phone number"
            )
        ]
    )

    def __str__(self):
        return self.username

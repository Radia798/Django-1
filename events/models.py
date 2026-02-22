from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events",
        null=True,
        blank=True
    )

    rsvp_users = models.ManyToManyField(
        User,
        related_name="rsvp_events",
        blank=True
    )

    image = models.ImageField(
        upload_to="event_images/",
        default="default_event.jpg"
    )

    def __str__(self):
        return self.name

from djongo import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Film(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in minutes")
    rating = models.FloatField(help_text="Rating from 1 to 10")
    description = models.TextField()
    # actors = models.ArrayField(models.CharField(max_length=100), blank=True)
    added_on = models.DateTimeField(default=timezone.now)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Rental(models.Model):
    rent_date = models.DateField(auto_now_add=True)
    planned_return_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return self.film.title

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

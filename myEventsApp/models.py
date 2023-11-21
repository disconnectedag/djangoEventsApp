from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    host = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    attendees = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myEventsApp:event_details', args=[self.id])


class Comment(models.Model):
    event = models.ForeignKey(Event, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    body = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s: %s' % (self.event.title, self.body, self.name)


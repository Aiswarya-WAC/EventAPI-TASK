from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    RECURRENCE_CHOICES = [
        ("None", "None"),
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
    ]
    recurrence = models.CharField(max_length=50,choices=RECURRENCE_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    recurrence_end_date = models.DateTimeField()
    duration = models.IntegerField()

    def __str__(self):
            return f"{self.title} - {self.user}"



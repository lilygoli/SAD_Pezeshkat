from django.db import models
from django.urls import reverse

from accounts.models import User


class Event(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default='reserved')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('doctor_calendar:calendar', args=(self.id,))
        return f'<p>{self.title}</p><a href="{url}">edit</a>'  # todo edit??
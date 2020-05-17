from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels
import jdatetime
from accounts.models import User


class Event(models.Model):
    doctor_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    patient_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_name')  # todo error if patient = doctor
    title = models.CharField(max_length=100)
    description = models.TextField(default='reserved')
    start_time = jmodels.jDateField(null=True)
    end_time = jmodels.jDateField(null=True)
    start_hour = models.FloatField(null=True)
    duration = models.FloatField(default=1)


    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('doctor_calendar:calendar', args=(self.doctor_user.id,))
        return f'<p>{self.title}</p><a href="{url}">edit</a>'  # todo edit??




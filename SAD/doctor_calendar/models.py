from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels

from accounts.models import User, DoctorProfileInfo, PatientProfileInfo


class Event(models.Model):
    doctor_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    patient_user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                     related_name='%(class)s_requests_name')  # todo error if patient = doctor
    title = models.CharField(max_length=100)
    description = models.TextField(default='reserved')
    start_time = jmodels.jDateField(null=True)
    start_hour = models.FloatField(null=True)

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        return f'<p class="cal-title">{self.title}' \
               f'</p><button onclick="return clicked(event,' + str(self.patient_user.pk)+',' + str(self.pk) +\
               ')">لغو</button>'


class CalenderWeekClicks(models.Model):
    doctor_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    patient_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    number_clicks = models.IntegerField()


class DoctorCalenderWeekClicks(models.Model):
    doctor_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    number_clicks = models.IntegerField()

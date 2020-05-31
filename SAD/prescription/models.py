from django.db import models

from accounts.models import User
from django_jalali.db import models as jmodels
from doctor_calendar.models import Event


class Prescriptions(models.Model):
    doctor = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    patient = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    appointment = models.ForeignKey(to=Event, on_delete=models.CASCADE, related_name='%(class)s_requests_event')

    class Meta:
        unique_together = ('doctor', 'patient', 'appointment')


class Tests(models.Model):
    prescription = models.ForeignKey(to=Prescriptions, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    deadline = jmodels.jDateField(null=False)


class Medicine(models.Model):
    prescription = models.ForeignKey(to=Prescriptions, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    starting_time = jmodels.jDateField(null=True)
    starting_hour = models.FloatField(null=True)
    time_interval = models.FloatField(null=True)
    status = models.BooleanField(default=False)
    total_dosage = models.IntegerField(null=True)
    dosage_every_time = models.IntegerField(null=True)
    times_left = models.IntegerField(null=True)


class Injections(models.Model):
    prescription = models.ForeignKey(to=Prescriptions, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    deadline = jmodels.jDateField(null=False)





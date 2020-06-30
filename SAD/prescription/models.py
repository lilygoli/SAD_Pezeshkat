from django.core.validators import MinValueValidator
from django.db import models
from django_jalali.db import models as jmodels

from accounts.models import User
from doctor_calendar.models import Event


class Prescriptions(models.Model):
    doctor = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    patient = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    appointment = models.ForeignKey(to=Event, on_delete=models.CASCADE, related_name='%(class)s_requests_event')
    comment = models.CharField(max_length=1000, default="")

    class Meta:
        unique_together = ('doctor', 'patient', 'appointment')


class Tests(models.Model):
    prescription = models.ForeignKey(to=Prescriptions, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    form_row = models.IntegerField(null=False)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    deadline = jmodels.jDateField(null=False)


class Medicine(models.Model):
    prescription = models.ForeignKey(to=Prescriptions, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    form_row = models.IntegerField(null=False)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    starting_time = jmodels.jDateField(null=True)
    starting_hour = models.TimeField(null=True)
    time_interval = models.FloatField(null=False)
    status = models.BooleanField(default=False)
    total_dosage = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    dosage_every_time = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    dosage_remaining = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    times_left = models.IntegerField(null=True)
    finished = models.BooleanField(default=False)


class Injections(models.Model):
    prescription = models.ForeignKey(to=Prescriptions, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    form_row = models.IntegerField(null=False)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    deadline = jmodels.jDateField(null=False)

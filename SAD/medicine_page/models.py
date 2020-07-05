from django.core.validators import MinValueValidator
from django.db import models

from django_jalali.db import models as jmodels

from accounts.models import User


class SelfAddedMedicine(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    starting_time = jmodels.jDateField(null=True)
    starting_hour = models.TimeField(null=True)
    time_interval = models.FloatField(null=False)
    status = models.BooleanField(default=True)
    total_dosage = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    dosage_every_time = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    dosage_remaining = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    times_left = models.IntegerField(null=True)
    finished = models.BooleanField(default=False)
    send_notification = models.BooleanField(default=False)
    number = models.IntegerField(default=0)

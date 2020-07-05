from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from accounts.models import User


class Rating(models.Model):
    doctor = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    patient = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_requests_name')
    score = models.FloatField(validators=[MaxValueValidator(5), MinValueValidator(0)])

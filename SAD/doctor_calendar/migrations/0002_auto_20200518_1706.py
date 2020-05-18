# Generated by Django 3.0.5 on 2020-05-18 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor_calendar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.CreateModel(
            name='DoctorCalenderWeekClicks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_clicks', models.IntegerField()),
                ('doctor_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctorcalenderweekclicks_requests_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CalenderWeekClicks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_clicks', models.IntegerField()),
                ('doctor_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calenderweekclicks_requests_created', to=settings.AUTH_USER_MODEL)),
                ('patient_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calenderweekclicks_requests_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

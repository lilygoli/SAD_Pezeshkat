# Generated by Django 3.0.5 on 2020-05-20 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default='reserved')),
                ('start_time', django_jalali.db.models.jDateField(null=True)),
                ('start_hour', models.FloatField(null=True)),
                ('doctor_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_requests_created', to=settings.AUTH_USER_MODEL)),
                ('patient_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_requests_name', to=settings.AUTH_USER_MODEL)),
            ],
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
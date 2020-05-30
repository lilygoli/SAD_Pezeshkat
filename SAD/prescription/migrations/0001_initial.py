# Generated by Django 3.0.5 on 2020-05-23 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor_calendar', '0003_auto_20200523_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_requests_event', to='doctor_calendar.Event')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_requests_created', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions_requests_name', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('deadline', django_jalali.db.models.jDateField()),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests_requests_name', to='prescription.Prescriptions')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('starting_time', django_jalali.db.models.jDateField(null=True)),
                ('starting_hour', models.FloatField(null=True)),
                ('time_interval', models.FloatField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('total_dosage', models.IntegerField(null=True)),
                ('dosage_every_time', models.IntegerField(null=True)),
                ('times_left', models.IntegerField(null=True)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicine_requests_name', to='prescription.Prescriptions')),
            ],
        ),
        migrations.CreateModel(
            name='Injections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('deadline', django_jalali.db.models.jDateField()),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='injections_requests_name', to='prescription.Prescriptions')),
            ],
        ),
    ]

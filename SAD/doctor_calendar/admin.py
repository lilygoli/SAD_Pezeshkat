from django.contrib import admin
from .models import Event, CalenderWeekClicks, DoctorCalenderWeekClicks

admin.site.register(Event)
admin.site.register(CalenderWeekClicks)
admin.site.register(DoctorCalenderWeekClicks)

from datetime import datetime as dt

from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic import ListView

from .models import *
from .utils import Calendar


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return year, month, 1
    return dt.today().year, dt.today().month, dt.today().day


class CalendarView(ListView):
    model = Event
    template_name = 'calendar/calendar.html'

    def get_doctor(self, request, pk):
        return get_object_or_404(User, id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))  # todo shamsi
        doc = self.kwargs['pk']
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d[0], d[1], d[2], doc)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        # print(context)
        return context


class DoctorCalenderView(ListView):
    model = Event
    template_name = 'calendar/doctor_calender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))  # todo shamsi
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d[0], d[1], d[2], self.request.user.pk)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        # print(context)
        return context

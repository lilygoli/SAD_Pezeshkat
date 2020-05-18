from datetime import datetime as dt

from django.utils.safestring import mark_safe
from django.views.generic import ListView

from .models import *
from .utils import Calendar


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return year, month, 1
    return dt.today().year, dt.today().month, dt.today().day


class PatientCalendarView(ListView):
    model = Event
    template_name = 'calendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        doc = self.kwargs['pk']
        try:
            clicks = CalenderWeekClicks.objects.get(doctor_user=doc, patient_user=self.request.user.id)
            back_or_forward = clicks.number_clicks
        except Exception:
            clicks = CalenderWeekClicks(doctor_user_id=doc, patient_user_id=self.request.user.id, number_clicks=0)
            clicks.save()
            back_or_forward = 0

        # Instantiate our calendar class with today's year and date
        if self.kwargs['week_num'] == '1':
            back_or_forward += 1
        elif self.kwargs['week_num'] == '2':
            back_or_forward -= 1
        else:
            back_or_forward = 0
        clicks.number_clicks = back_or_forward
        clicks.save()
        cal = Calendar(d[0], d[1], d[2], doc, curr_user=self.request.user, offset=back_or_forward)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.format_month()
        context['calendar'] = mark_safe(html_cal)
        context['doctor'] = doc
        return context


class DoctorCalenderView(ListView):
    model = Event
    template_name = 'calendar/doctor_calender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        try:
            clicks = DoctorCalenderWeekClicks.objects.get(doctor_user=self.request.user)
            back_or_forward = clicks.number_clicks
        except Exception:
            clicks = DoctorCalenderWeekClicks(doctor_user=self.request.user, number_clicks=0)
            clicks.save()
            back_or_forward = 0
        # Instantiate our calendar class with today's year and date
        if self.kwargs['week_num'] == '1':
            back_or_forward += 1
        elif self.kwargs['week_num'] == '2':
            back_or_forward -= 1
        else:
            back_or_forward = 0
        clicks.number_clicks = back_or_forward
        clicks.save()

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d[0], d[1], d[2], self.request.user.pk, curr_user=self.request.user, offset=back_or_forward)
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.format_month()
        context['calendar'] = mark_safe(html_cal)
        # print(context)
        return context


class VerifyView(ListView):
    # model = DoctorProfileInfo
    template_name = 'calendar/verify.html'


    def get_queryset(self):
        query_name = self.request.GET.get('q1')
        dateAndTime = query_name.split('#')
        date = dateAndTime[0].split("-")
        # print(self.kwargs['pk'])
        s = Event(doctor_user=User.objects.filter(pk=self.kwargs['pk'])[0], patient_user=self.request.user, title='reserved',
                  start_time=jdatetime.date(int(date[0]), int(date[1]), int(date[2])),
                  start_hour=dateAndTime[1])
        s.save()



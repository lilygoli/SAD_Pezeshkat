from datetime import datetime as dt

import jdatetime
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.views.generic import ListView

from .models import *
from .utils import Calendar

PERCENT = 0.10


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
        clicks, _ = CalenderWeekClicks.objects.get_or_create(doctor_user_id=doc, patient_user_id=self.request.user.id)
        back_or_forward = clicks.number_clicks
        # try:
        #     clicks = CalenderWeekClicks.objects.get(doctor_user=doc, patient_user=self.request.user.id)
        #     back_or_forward = clicks.number_clicks
        # except Exception:
        #     clicks = CalenderWeekClicks(doctor_user_id=doc, patient_user_id=self.request.user.id, number_clicks=0)
        #     clicks.save()
        #     back_or_forward = 0

        if self.kwargs['week_num'] == '0':
            back_or_forward = 0

        clicks.number_clicks = back_or_forward
        clicks.save()
        cal = Calendar(d[0], d[1], d[2], doc, curr_user=self.request.user, offset=back_or_forward)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.format_month()
        context['calendar'] = mark_safe(html_cal)
        context['doctor'] = doc
        return context


def next_week(request, pk, week_num):
    doc = pk
    clicks, _ = CalenderWeekClicks.objects.get_or_create(doctor_user_id=doc, patient_user_id=request.user.id)
    back_or_forward = clicks.number_clicks
    # try:
    #     clicks = CalenderWeekClicks.objects.get(doctor_user=doc, patient_user=request.user.id)
    #     back_or_forward = clicks.number_clicks
    # except Exception:
    #     clicks = CalenderWeekClicks(doctor_user_id=doc, patient_user_id=request.user.id, number_clicks=0)
    #     clicks.save()
    #     back_or_forward = 0

        # Instantiate our calendar class with today's year and date
    if week_num == '1':
        back_or_forward += 1
    elif week_num == '2':
        back_or_forward -= 1
    elif week_num == '0':
        back_or_forward = 0

    clicks.number_clicks = back_or_forward
    clicks.save()
    return redirect('doctor_calendar:calendar', pk=doc, week_num=3)


def doctor_next_week(request, week_num):
    doc = request.user
    clicks, _ = DoctorCalenderWeekClicks.objects.get_or_create(doctor_user_id=doc)
    back_or_forward = clicks.number_clicks
    # try:
    #     clicks = DoctorCalenderWeekClicks.objects.get(doctor_user=doc)
    #     back_or_forward = clicks.number_clicks
    # except Exception:
    #     clicks = DoctorCalenderWeekClicks.objects.get(doctor_user=doc, number_clicks=0)
    #     clicks.save()
    #     back_or_forward = 0

        # Instantiate our calendar class with today's year and date
    if week_num == '1':
        back_or_forward += 1
    elif week_num == '2':
        back_or_forward -= 1
    elif week_num == '0':
        back_or_forward = 0

    clicks.number_clicks = back_or_forward
    clicks.save()
    return redirect('doctor_calendar:schedule', week_num=3)


class DoctorCalenderView(ListView):
    model = Event
    template_name = 'calendar/doctor_calender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        doc = self.request.user.id
        clicks, _ = DoctorCalenderWeekClicks.objects.get_or_create(doctor_user_id=doc)
        back_or_forward = clicks.number_clicks
        # try:
        #     clicks = DoctorCalenderWeekClicks.objects.get(doctor_user_id=doc)
        #     back_or_forward = clicks.number_clicks
        # except Exception:
        #     clicks = DoctorCalenderWeekClicks(doctor_user_id=doc, number_clicks=0)
        #     clicks.save()
        #     back_or_forward = 0

        if self.kwargs['week_num'] == '0':
            back_or_forward = 0
        clicks.number_clicks = back_or_forward
        clicks.save()

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d[0], d[1], d[2], self.request.user.pk, curr_user=self.request.user, offset=back_or_forward)
        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.format_month()
        context['calendar'] = mark_safe(html_cal)
        return context


class VerifyView(ListView):
    template_name = 'calendar/verify.html'
    is_successful = False
    doctor = None
    date = None
    time = None

    def get_queryset(self):
        me = User.objects.get(is_staff=True)
        query_name = self.request.GET.get('q1')
        date_and_time = query_name.split('#')
        date = date_and_time[0].split("-")
        self.date = date
        self.time = date_and_time[1]
        doctor = DoctorProfileInfo.objects.get(user_id=self.kwargs['pk'])
        self.doctor = doctor
        patient = PatientProfileInfo.objects.get(user_id=self.request.user)

        if patient.credit < doctor.fee:
            self.is_successful = False
        else:
            doctor.credit += doctor.fee
            patient.credit -= doctor.fee
            me.bank += doctor.fee / 10
            print(me.bank)
            me.save()
            doctor.save()
            patient.save()
            s = Event(doctor_user=User.objects.filter(pk=self.kwargs['pk'])[0], patient_user=self.request.user,
                      title='reserved',
                      start_time=jdatetime.date(int(date[0]), int(date[1]), int(date[2])),
                      start_hour=date_and_time[1])
            s.save()
            self.is_successful = True

    def get_context_data(self, **kwargs):
        context = {
            'success': self.is_successful,
            'address': self.doctor.address,
            'name': self.doctor.user.name,
            'lname': self.doctor.user.family_name,
            'day': self.date[2],
            'month': self.date[1],
            'year': self.date[0],
            'hour': self.time,
            'doc_pk': self.doctor.user.pk

        }

        return context


def cancel(request, doc_pk, usr_pk, evt_pk):
    event = Event.objects.get(id=evt_pk)
    doctor = DoctorProfileInfo.objects.get(user_id=doc_pk)
    try:
        patient = PatientProfileInfo.objects.get(user_id=usr_pk)
    except Exception:
        patient = DoctorProfileInfo.objects.get(user_id=usr_pk)
    doctor.credit -= doctor.fee * (1 - PERCENT)
    patient.credit += doctor.fee * (1 - PERCENT)
    doctor.save()
    patient.save()
    event.delete()

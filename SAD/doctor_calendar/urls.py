from django.conf.urls import url
from doctor_calendar import views as v

app_name = 'doctor_calendar'
urlpatterns = [
    url(r'^calendar/(?P<pk>\d+)$', v.PatientCalendarView.as_view(), name='calendar'),
    # url(r'^doctor-schedule/', v., name='schedule'),
    url(r'^schedule/', v.DoctorCalenderView.as_view(), name='schedule')
]

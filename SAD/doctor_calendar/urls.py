from django.conf.urls import url
from doctor_calendar import views as v

app_name = 'doctor_calendar'
urlpatterns = [
    url(r'^calendar/(?P<pk>\d+)/(?P<week_num>\d+)$', v.PatientCalendarView.as_view(), name='calendar'),
    url(r'^schedule/(?P<week_num>\d+)$', v.DoctorCalenderView.as_view(), name='schedule'),
    url(r'^verify/(?P<pk>\d+)/(?P<week_num>\d+)$', v.VerifyView.as_view(), name='verify'),
]

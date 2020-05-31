from prescription import views as v
from django.conf.urls import url

app_name = 'prescription'
urlpatterns = [
    url(r'^prescription/(?P<prescription_id>\d+)/$', v.write_prescription, name='prescription'),
    url(r'^make-prescription/(?P<doc_id>\d+)/(?P<patient_id>\d+)/(?P<event_id>\d+)$', v.make_prescription, name='make-prescription'),
]


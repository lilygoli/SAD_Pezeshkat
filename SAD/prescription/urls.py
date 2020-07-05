from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from prescription import views as v

app_name = 'prescription'
urlpatterns = [
    url(r'^prescription/(?P<prescription_id>\d+)/(?P<cal>\d+)/$', v.write_prescription, name='prescription'),
    url(r'prescription/(?P<prescription_id>\d+)/(?P<cal>\d+)/delete-med/(?P<med_id>\d+)/(?P<med_type>\d+)', v.delete_med, name='delete-med'),
    url(r'^make-prescription/(?P<doc_id>\d+)/(?P<patient_id>\d+)/(?P<event_id>\d+)$', v.make_prescription,
        name='make-prescription'),
    url(r'^prescription_list/(?P<pk>\d+)', login_required(v.PrescriptionListView.as_view()), name='pre_list'),
    url(r'^prescription_list_patient/(?P<pk>\d+)', login_required(v.PrescriptionListPatientView.as_view()),
        name='pre_list_patient')

]

from django.conf.urls import url

from prescription import views as v

app_name = 'prescription'
urlpatterns = [
    url(r'^prescription/(?P<prescription_id>\d+)/(?P<cal>\d+)$', v.write_prescription, name='prescription'),
    url(r'prescription/(?P<prescription_id>\d+)/delete-med/(?P<med_id>\d+)', v.delete_med, name='delete-med'),
    url(r'prescription/(?P<prescription_id>\d+)/delete-test/(?P<test_id>\d+)', v.delete_test, name='delete-test'),
    url(r'prescription/(?P<prescription_id>\d+)/delete-injection/(?P<inj_id>\d+)', v.delete_injection, name='delete-injection'),
    url(r'^make-prescription/(?P<doc_id>\d+)/(?P<patient_id>\d+)/(?P<event_id>\d+)$', v.make_prescription,
        name='make-prescription'),
]

from django.conf.urls import url
from patient_list import views as v

app_name = 'patient_list'
urlpatterns = [
    url(r'^list/', v.PatientListView.as_view(), name='list')
]

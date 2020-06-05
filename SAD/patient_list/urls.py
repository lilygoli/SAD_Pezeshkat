from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from patient_list import views as v

app_name = 'patient_list'
urlpatterns = [
    url(r'^list/',login_required(v.PatientListView.as_view()), name='list')
]

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from prescription_list_patient import views as v

app_name = 'prescription_list_patient'
urlpatterns = [
    url(r'^prescription_list_patient/(?P<pk>\d+)', login_required(v.PrescriptionListPatientView.as_view()), name='pre_list_patient')
]

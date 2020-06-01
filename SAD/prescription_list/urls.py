from django.conf.urls import url
from prescription_list import views as v

app_name = 'prescription_list'
urlpatterns = [
    url(r'^prescription_list/(?P<pk>\d+)', v.PrescriptionListView.as_view(), name='pre_list')
]

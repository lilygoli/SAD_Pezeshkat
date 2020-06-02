from django.conf.urls import url
from visit_history import views as v

app_name = 'visit_history'
urlpatterns = [
    url(r'^visit_history/', v.DoctorListView.as_view(), name='history')
]

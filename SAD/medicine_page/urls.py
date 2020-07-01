from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from medicine_page import views as v

app_name = 'medicine_page'
urlpatterns = [
    url(r'^medicine_page/', login_required(v.MedicineListView.as_view()), name='medicines'),
    url(r'^start_notif/(?P<med_id>\d+)/', v.set_start_time, name='start_notif'),
    url(r'^medicine_page/disable-notif/(?P<med_id>\d+)/', v.disable_notif, name='disable_notif'),

]
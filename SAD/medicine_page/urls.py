from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from medicine_page import views as v

app_name = 'medicine_page'
urlpatterns = [
    url(r'^medicine_page/disable-notif/(?P<med_id>\d+)/', v.disable_notif, name='disable-notif'),
    url(r'^medicine_page/disable-self-notif/(?P<med_id>\d+)/', v.disable_self_notif, name='disable-self-notif'),
    url(r'^medicine_page/$', login_required(v.MedicineListView.as_view()), name='medicines'),
    url(r'^start_notif/(?P<med_id>\d+)/(?P<self>\d+)/', v.set_start_time, name='start_notif'),
    url(r'^add_med/', v.add_med, name='add_med'),
    url(r'^delete_med/(?P<med_id>\d+)', v.delete_med, name='delete_med'),

]

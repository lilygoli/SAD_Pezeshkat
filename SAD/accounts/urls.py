from accounts import views as v
from django.conf.urls import url

app_name = 'accounts'
urlpatterns=[
    url(r'^profile/edit/$', v.edit_profile, name='edit_profile'),
    url(r'^register/$', v.register, name='register'),
    url(r'^user_login/$', v.user_login, name='user_login'),
    url(r'^logout/$', v.user_logout, name='logout'),
    url(r'^special/', v.special, name='special'),
    url(r'^$', v.index, name='index'),
]

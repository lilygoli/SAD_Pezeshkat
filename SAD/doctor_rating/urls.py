from django.conf.urls import url

import doctor_rating.views as v

app_name = 'doctor_rating'
urlpatterns = [
    url(r'^rate/', v.rate, name='rate'),
]

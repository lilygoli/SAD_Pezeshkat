"""SAD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts import urls as u1
from doctor_calendar import urls as u3
from doctor_rating import urls as u9
from medicine_page import urls as u10
from doctor_search import urls as u2
from patient_list import urls as u4
from prescription import urls as u5
from prescription_list import urls as u6
from prescription_list_patient import urls as u8
from visit_history import urls as u7

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(u1)),
                  path('', include(u2)),
                  path('', include(u3)),
                  path('', include(u4)),
                  path('', include(u5)),
                  path('', include(u6)),
                  path('', include(u7)),
                  path('', include(u8)),
                  path('', include(u9)),
                  path('', include(u10)),
                  path('accounts/', include('django.contrib.auth.urls')),
              ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

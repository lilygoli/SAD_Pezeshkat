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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf.urls.static import static
from accounts import urls as u1
from doctor_search import urls as u2

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^login/$', auth_views.auth_login, name='login'),
    # url(r'^logout/$', auth_views.auth_logout, name='logout'),
    # path('', my_view, name='login')

    path('', include(u1)),
    path('', include(u2)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

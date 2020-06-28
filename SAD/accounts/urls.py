from accounts import views as v
from django.conf.urls import url
from django.urls import path, include
from accounts.forms import UserSetPassword, UserPasswordChange
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             form_class=UserSetPassword), name='password_reset_confirm'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_change/',
        auth_views.PasswordChangeView.as_view(
            form_class=UserPasswordChange), name='password_change'),
    url(r'^profile/edit/$', v.edit_profile, name='edit_profile'),
    url(r'^register/$', v.register, name='register'),
    url(r'^user_login/$', v.user_login, name='user_login'),
    url(r'^logout/$', v.user_logout, name='logout'),
    url(r'^special/', v.special, name='special'),
    url(r'^$', v.index, name='index'),
    url(r'^mini_profile/(?P<pk>\d+)$', v.mini_profile, name='mini_profile'),
    url(r'monthly_income$', v.monthly_income, name='monthly_income'),

]

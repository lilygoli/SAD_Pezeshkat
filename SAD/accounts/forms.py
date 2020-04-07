from django import forms
from accounts.models import User, UserProfileInfo


# from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password.label = "رمزعبور"

    class Meta():
        model = User
        fields = ('name', 'password', 'email')
        labels = {
            "name": "نام",
            "password": "رمزعبور",
            "email": "ایمیل"
        }


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic', 'height', 'weight')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            "height": "قد",
            "weight": "وزن"
        }

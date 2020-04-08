from django import forms
from accounts.models import User, UserProfileInfo


# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password.label = "رمزعبور"

    class Meta:
        model = User
        fields = ('name', 'password', 'email')
        labels = {
            "name": "نام",
            "password": "رمزعبور",
            "email": "ایمیل"
        }


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic', 'height', 'weight')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            "height": "قد",
            "weight": "وزن"
        }


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('name', 'email')
        labels = {
            "name": "نام",
            "email": "ایمیل",
        }


class EditProfileInfo(UserChangeForm):
    password = None

    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic', 'height', 'weight')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            "height": "قد",
            "weight": "وزن"
        }

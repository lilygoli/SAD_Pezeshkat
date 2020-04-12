from django import forms
from accounts.models import User, DoctorProfileInfo, PatientProfileInfo

# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password.label = "رمزعبور"

    class Meta:
        model = User
        fields = ('name', 'email', 'password','is_doctor')
        labels = {
            "name": "نام",
            "password": "رمزعبور",
            "email": "ایمیل",
        }


class DoctorProfileInfoForm(forms.ModelForm):
    class Meta:
        model = DoctorProfileInfo
        fields = (
        'portfolio_site', 'profile_pic', 'specialty', 'degree', 'educational_background', 'fee', 'on_site_fee',
        'address', 'score')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            'specialty': "تخصص",
            'degree': 'درجه پزشکی',
            'educational_background': "پیشینه تحصیلی",
            'fee': "حق ویزیت",
            'on_site_fee': "مشخص شدن و قابلیت پرداخت حق ویزیت در مطب",
            'address': "آدرس",
            'score': "امتیاز"
        }


class PatientProfileInfoFrom(forms.ModelForm):
    class Meta:
        model = PatientProfileInfo
        fields = (
         'profile_pic', 'birthday', 'medical_condition', 'medical_emergency_contact', 'credit',
        'blood_type', 'blood_plus_minus', 'allergies', 'height', 'weight')
        labels = {
            "profile_pic": "عکس",
            'birthday': "تاریخ تولد",
            'medical_condition': "بیماری ها",
            'medical_emergency_contact': "شماره تلفن موارد پزشکی اضطراری",
            'credit':'اعتبار' ,
            'blood_type':'گروه خونی' ,
            'blood_plus_minus':'گروه خونی مثبت/منفی' ,
            'allergies': 'حساسیت ها',
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


class PatientEditProfileInfo(UserChangeForm):
    password = None

    class Meta:
        model = PatientProfileInfo
        fields = (
            'profile_pic', 'birthday', 'medical_condition', 'medical_emergency_contact', 'credit',
            'blood_type', 'blood_plus_minus', 'allergies', 'height', 'weight')
        labels = {
            "profile_pic": "عکس",
            'birthday': "تاریخ تولد",
            'medical_condition': "بیماری ها",
            'medical_emergency_contact': "شماره تلفن موارد پزشکی اضطراری",
            'credit': 'اعتبار',
            'blood_type': 'گروه خونی',
            'blood_plus_minus': 'گروه خونی مثبت/منفی',
            'allergies': 'حساسیت ها',
            "height": "قد",
            "weight": "وزن"
        }


class DoctorEditProfileInfo(UserChangeForm):
    password = None

    class Meta:
        model = DoctorProfileInfo
        fields = (
            'portfolio_site', 'profile_pic', 'specialty', 'degree', 'educational_background', 'fee', 'on_site_fee',
            'address', 'score')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            'specialty': "تخصص",
            'degree': 'درجه پزشکی',
            'educational_background': "پیشینه تحصیلی",
            'fee': "حق ویزیت",
            'on_site_fee': "مشخص شدن و قابلیت پرداخت حق ویزیت در مطب",
            'address': "آدرس",
            'score': "امتیاز"
        }


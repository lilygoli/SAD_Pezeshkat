from django import forms
from django.core.exceptions import ValidationError

from accounts.email_domians import DOMAINS
from accounts.models import User, DoctorProfileInfo, PatientProfileInfo

# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password.label = "رمزعبور"

    class Meta:
        model = User
        fields = ('name', 'family_name', 'email', 'password', 'is_doctor')
        labels = {
            "name": "نام",
            "family_name": "نام خانوادگی",
            "password": "رمزعبور",
            "email": "ایمیل",
        }

    def is_valid(self):
        valid = super(UserForm, self).is_valid()
        email = self.data['email']
        password = self.data['password']
        valid2 = True
        if '@' not in email:
            valid2 = False
        else:
            x = email.split('@')
            if len(x) != 2:
                valid2 = False
            else:
                dom = x[1]
                if '.' not in dom:
                    print(dom)
                    valid2 = False
                else:

                    if dom not in DOMAINS:
                        valid2 = False
        if not valid2:
            self.add_error('email', 'ایمیل نامعتبر')
        if len(password) < 6:
            valid2 = False
            self.add_error('password', 'رمز عبور باید بیشتر از 5 کاراکتر باشد.')
        if password.isnumeric() or password.isalpha():
            valid2 = False
            self.add_error('password', 'رمز عبور باید دارای حداقل یک عدد و یک کاراکتر الفبا باشد.')
        if "٫×÷\"!@#$%^&*)(_+-=|{}\[],؛،ـ«»:<>؟/~`;'.?" in password:
            valid2 = False
            self.add_error('password', 'رمز عبور باید فقط از عدد یا الفبا تشکیل شده باشد.')
        return valid and valid2


class DoctorProfileInfoForm(forms.ModelForm):
    class Meta:
        model = DoctorProfileInfo
        fields = (
            'portfolio_site', 'profile_pic', 'specialty_bins','specialty', 'degree', 'educational_background', 'fee', 'on_site_fee',
            'address', 'score')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            "specialty_bins": "دسته تخصص",
            "specialty": "تخصص",
            "degree": 'درجه پزشکی',
            "educational_background": "پیشینه تحصیلی",
            "fee": "حق ویزیت",
            "on_site_fee": "مشخص شدن و قابلیت پرداخت حق ویزیت در مطب",
            "address": "آدرس",
            "score": "امتیاز"
        }


class PatientProfileInfoFrom(forms.ModelForm):
    class Meta:
        model = PatientProfileInfo
        fields = (
            'profile_pic', 'birthday', 'medical_condition', 'medical_emergency_contact',
            'blood_type', 'blood_plus_minus', 'allergies', 'height', 'weight')
        widgets = {
            'birthday': DateInput()
        }
        labels = {
            "profile_pic": "عکس",
            "birthday": "تاریخ تولد",
            "medical_condition": "بیماری ها",
            "medical_emergency_contact": "شماره تلفن موارد پزشکی اضطراری",
            'credit': 'اعتبار',
            'blood_type': 'گروه خونی',
            'blood_plus_minus': 'گروه خونی مثبت/منفی',
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

    def save(self, commit=True):
        if self.is_valid():
            # Get instance with self.instance & only update if a value's changed:
            for field_name in self.fields:
                if getattr(self.instance, field_name) != self.cleaned_data[field_name]:
                    setattr(self.instance, field_name, self.cleaned_data[field_name])
                    self.instance.save()
        return self.instance


class DoctorEditProfileInfo(UserChangeForm):
    password = None

    class Meta:
        model = DoctorProfileInfo
        fields = (
            'portfolio_site', 'profile_pic', 'specialty', 'degree', 'educational_background', 'fee', 'on_site_fee',
            'address')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            'specialty': "تخصص",
            'degree': 'درجه پزشکی',
            'educational_background': "پیشینه تحصیلی",
            'fee': "حق ویزیت",
            'on_site_fee': "مشخص شدن و قابلیت پرداخت حق ویزیت در مطب",
            'address': "آدرس",
        }

    def save(self, commit=True):
        if self.is_valid():
            # Get instance with self.instance & only update if a value's changed:
            for field_name in self.fields:
                if getattr(self.instance, field_name) != self.cleaned_data[field_name]:
                    setattr(self.instance, field_name, self.cleaned_data[field_name])
                    self.instance.save()
        return self.instance

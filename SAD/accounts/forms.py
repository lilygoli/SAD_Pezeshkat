from django import forms
from django.core.exceptions import ValidationError

from accounts.email_domians import DOMAINS
from accounts.models import User, DoctorProfileInfo, PatientProfileInfo
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm


class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password.label = "رمزعبور"
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ('name', 'family_name', 'email', 'password', 'is_doctor')
        labels = {
            "name": "نام",
            "family_name": "نام خانوادگی",
            "password": "رمزعبور",
            "email": "ایمیل",
        }

    def clean(self):
        super(UserForm, self).clean()
        email = self.cleaned_data['email']  # adding some extra validation criteria to django's email validation!!
        email_parts = email.split('@')
        valid = True
        if len(email_parts) != 2:
            valid = False
        else:
            dom = email_parts[1]
            if '.' not in dom:
                valid = False
            else:
                if dom not in DOMAINS:
                    valid = False
        errors = {'email': [], 'password': []}
        if not valid:
            errors['email'] += ['ایمیل نامعتبر است.']
        password = self.cleaned_data['password']
        try:
            password_validation.validate_password(password)
        except ValidationError as error:
            print(error.error_list)
            errors['password'] += error.error_list
        if len(errors['email']) > 0 or len(errors['password']) > 0:
            raise ValidationError(errors)


class DoctorProfileInfoForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = DoctorProfileInfo
        fields = (
            'portfolio_site', 'profile_pic', 'specialty_bins', 'specialty', 'degree', 'educational_background', 'fee',
            'on_site_fee',
            'address', 'score')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            "specialty_bins": "دسته تخصص",
            "specialty": "تخصص",
            "degree": 'درجه پزشکی',
            "educational_background": "پیشینه تحصیلی",
            "fee": "حق ویزیت",
            "on_site_fee": "مشخص شدن حق ویزیت در مطب",
            "address": "آدرس",
            "score": "امتیاز"
        }

    def clean(self):
        errors = {'specialty_bins': [], 'fee': []}
        if self.cleaned_data['specialty_bins'] == "-" and self.cleaned_data['specialty'] is None:
            errors['specialty_bins'] += ['لطفا دسته‌ی تخصص خود را مشخص کنید یا نام آن را در بخش تخصص بنویسید.']
        if not self.cleaned_data['fee'] and not self.cleaned_data['on_site_fee']:
            errors['fee'] += ['لطفا حق ویزیت را مشخص کنید یا گزینه "مشخص شدن حق ویزیت در مطب" را انتخاب کنید.']
        if len(errors['specialty_bins']) > 0 or len(errors['fee']) > 0:
            raise ValidationError(errors)


class PatientProfileInfoFrom(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

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


class UserSetPassword(SetPasswordForm):
    class Meta:
        model = User

    error_messages = {
        **SetPasswordForm.error_messages,
        'password_mismatch': 'تکرار رمز با رمز جدید یکسان نیست.'
    }
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'autofocus': True}),
        strip=False,

    )
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
    )


class UserPasswordChange(PasswordChangeForm):
    class Meta:
        model = User

    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': "رمز عبور قدیمی نادرست وارد شده است.",
        'password_mismatch' : 'تکرار رمز با رمز جدید یکسان نیست.'
    }
    old_password = forms.CharField(
        label="رمز عبور قدیمی",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
        help_text=''
    )

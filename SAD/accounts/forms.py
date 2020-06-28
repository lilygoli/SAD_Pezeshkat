import datetime
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from accounts.email_domians import DOMAINS
from accounts.models import User, DoctorProfileInfo, PatientProfileInfo

Inverse = {'ﭼﺸﻢ ﭘﺰﺷﮑﯽ': 'eye', 'ﺭﺍﺩﯾﻮﻟﻮﮊﯼ': 'ray', 'ﭘﻮﺳﺖ ﻭ ﻣﻮ': 'hair', "ﭘﺰﺷﮑﯽﻫﺴﺘﻪﺍﯼ": 'nuc', "ﺍﺭﺗﻮﭘﺪﯼ": 'ort',
               'ﻗﻠﺐﻭﻋﺮﻭﻕ': 'heart',
               'ﻃﺐ ﻓﯿﺰﯾﮑﯽ': 'fizik', 'ﻣﻐﺰﻭﺍﻋﺼﺎﺏ': 'brain', 'ﮔﻮﺵ ﺣﻠﻖ ﺑﯿﻨﯽ': 'ear', 'ﺟﺮﺍﺣﯽ ﻣﻐﺰﻭﺍﻋﺼﺎﺏ': 'brainsurg',
               'ﭘﺎﺗﻮﻟﻮﮊﯼ': 'path', 'ﮐﻠﯿﻪ ﻭ ﻣﺠﺎﺭﯼﺍﺩﺭﺍﺭﯼ': 'kidney', 'ﭘﺮﺗﻮﺩﺭﻣﺎﻧﯽ - ﺭﺍﺩﯾﻮﺗﺮﺍﭘﯽ': 'rayray',
               'ﺟﺮﺍﺣﯽ ﻋﻤﻮﻣﯽ': 'general', 'ﺯﻧﺎﻥ ﻭ ﺯﺍﯾﻤﺎﻥ': 'women', 'ﺭﻭﺍﻧﭙﺰﺷﮑﯽ': 'psych', 'ﺩﺍﺧﻠﯽ': 'in', 'ﻃﺐﮐﺎﺭ': 'work',
               'ﮐﻮﺩﮐﺎﻥ': 'kids', 'ﺑﯿﻬﻮﺷﯽ': 'faint', 'ﻋﻔﻮﻧﯽ': 'inf', '-': 'other'}

DAY_CHOICES = (
    ("0", "شنبه"),
    ("1", "یکشنبه"),
    ("2", "دوشنبه"),
    ("3", "سه شنبه"),
    ("4", "چهارشنبه"),
    ("5", "پنجشنبه"),
    ("6", "جمعه"),
)


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
    picked = forms.MultipleChoiceField(choices=DAY_CHOICES, widget=forms.CheckboxSelectMultiple(), label='روزهای کاری')

    class Meta:
        model = DoctorProfileInfo

        fields = (
            'portfolio_site', 'profile_pic', 'specialty_bins', 'specialty', 'degree', 'educational_background', 'fee',
            'on_site_fee',
            'address', 'picked', 'visit_duration', 'score', 'available_weekdays', 'start_hour', 'end_hour')
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
            "score": "امتیاز",
            'visit_duration': 'مدت زمان متوسط هر ویزیت',
            'available_weekdays': 'روزهای کاری ',
            'start_hour': 'ساعت سروع کار',
            'end_hour': 'ساعت پایان کار'
        }

    def clean_available_weekdays(self):
        picked = self.cleaned_data['picked']
        s = ''
        for i in range(7):
            if str(i) in picked:
                s += '1'
            else:
                s += '0'
        return s

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
        fields = ('name', 'family_name','email')
        labels = {
            "name": "نام",
            "email": "ایمیل",
            "family_name": "نام‌خانوادگی"
        }


class PatientEditProfileInfo(UserChangeForm):
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

    def __init__(self, *args, **kwargs):
        super(PatientEditProfileInfo, self).__init__(*args, **kwargs)
        del self.fields['password']


class DoctorEditProfileInfo(forms.ModelForm):
    available_weekdays = forms.MultipleChoiceField(choices=DAY_CHOICES, widget=forms.CheckboxSelectMultiple(), label='روزهای کاری')

    class Meta:
        model = DoctorProfileInfo
        fields = (
            'portfolio_site', 'profile_pic', 'specialty', 'degree', 'educational_background', 'fee', 'on_site_fee',
            'address','visit_duration', 'start_hour', 'end_hour', 'available_weekdays')
        labels = {
            "portfolio_site": "وبسایت شخصی",
            "profile_pic": "عکس",
            'specialty': "تخصص",
            'degree': 'درجه پزشکی',
            'educational_background': "پیشینه تحصیلی",
            'fee': "حق ویزیت",
            'on_site_fee': "مشخص شدن و قابلیت پرداخت حق ویزیت در مطب",
            'address': "آدرس",
            'visit_duration': 'مدت زمان متوسط هر ویزیت',
            'available_weekdays': 'روزهای کاری ',
            'start_hour': 'ساعت شروع کار',
            'end_hour': 'ساعت پایان کار'
        }

    def __init__(self, *args, **kwargs):
        super(DoctorEditProfileInfo, self).__init__(*args, **kwargs)

    def clean_available_weekdays(self):
        available_weekdays = self.cleaned_data['available_weekdays']
        s = ''
        for i in range(7):
            if str(i) in available_weekdays:
                s += '1'
            else:
                s += '0'
        return s


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
        'password_mismatch': 'تکرار رمز با رمز جدید یکسان نیست.'
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


class TimeInterval(forms.Form):
    start_date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(widget=DateInput(attrs={'class': 'datepicker'}))
    #todo errors

    # def clean(self):
    #     errors = {'end_date': []}
    #     cln = self.cleaned_data
    #     if cln['end_date'] - cln['start_date'] < datetime.timedelta(14) or\
    #             cln['end_date'] - cln['start_date'] > datetime.timedelta(60):
    #         errors['end_date'] += ['لطفا باازه زمانی‌ای بین ۲ هفته تا ۲ ماه را انتخاب کنید.']
    #     if len(errors['end_date']) > 0:
    #         raise ValidationError(errors)

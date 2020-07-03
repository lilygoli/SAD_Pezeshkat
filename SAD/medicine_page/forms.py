import datetime

from bootstrap_datepicker_plus import TimePickerInput
from django import forms
from django.utils.timezone import localtime, now

from medicine_page.models import SelfAddedMedicine
from prescription.models import Medicine


class StartMedFrom(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    prefix = 'med'
    dosage_remaining = forms.IntegerField(required=False)
    dosage_every_time = forms.IntegerField(required=False)

    class Meta:
        model = Medicine
        fields = (
            'starting_time', 'starting_hour', 'dosage_remaining', 'dosage_every_time'
        )

        widgets = {
            'starting_time': forms.DateInput(attrs={'class': 'datepicker'}),
            'starting_hour': TimePickerInput(),

        }

    def clean(self):
        clean_med(self)


class StartSelfMedFrom(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    prefix = 'med'
    dosage_remaining = forms.IntegerField(required=False)
    dosage_every_time = forms.IntegerField(required=False)

    class Meta:
        model = SelfAddedMedicine
        fields = (
            'starting_time', 'starting_hour', 'dosage_remaining', 'dosage_every_time'
        )

        widgets = {
            'starting_time': forms.DateInput(attrs={'class': 'datepicker'}),
            'starting_hour': TimePickerInput(),

        }

    def clean(self):
        clean_med(self)


def clean_med(self):
    clean_med_date(self)
    if 'dosage_remaining' in self.cleaned_data.keys() and 'dosage_every_time' in self.cleaned_data.keys() \
        and self.cleaned_data['dosage_remaining'] and self.cleaned_data['dosage_every_time']\
            and self.cleaned_data['dosage_every_time'] > self.cleaned_data['dosage_remaining']:
        if 'dosage_every_time' in self.errors.keys():
            self.errors['dosage_every_time'] += ['مقدار مصرف هر بار باید کوچکتر از مقدار مصرف کل باشد.']
        else:
            self.errors['dosage_every_time'] = ['مقدار مصرف هر بار باید کوچکتر از مقدار مصرف کل باشد.']


def clean_med_date(self):
    date = None
    if 'starting_time' in self.cleaned_data.keys():
        try:
            date = self.cleaned_data['starting_time'].togregorian()
        except:
            self.errors['starting_time'] = ['لطفا تاریخ شروع معتبر وارد کنید. (مثال: 1399-12-01)']
        if date:
            if date.year > 2000:
                if date < datetime.date.today():
                    self.errors['starting_time'] = ['تاریخ شروع باید امروز یا بعد از امروز باشد']
            else:
                self.errors['starting_time'] = ['لطفا تاریخ شروع معتبر وارد کنید. (مثال: 1399-12-01)']
    else:
        self.errors['starting_time'] = ['لطفا تاریخ شروع معتبر وارد کنید.']
    if 'starting_hour' in self.errors.keys():
        self.errors['starting_hour'] = ['لطفا تاریخ معتبر وارد کنید.']
    if date and date <= localtime(now()).date() and self.cleaned_data['starting_hour'] < localtime(now()).time():
        self.errors['starting_hour'] = ['زمان شروع باید از الان به بعد باشد.']


class SelfMedForm(forms.ModelForm):
    prefix = 'self-med'
    description = forms.CharField(required=False)

    class Meta:
        model = SelfAddedMedicine
        fields = (
            'name', 'description', 'time_interval', 'dosage_every_time', 'total_dosage', 'starting_time',
            'starting_hour', 'status'
        )
        labels = {
            'name': 'نام',
            'description': 'توضیح',
            'time_interval': 'بازه زمانی بین دو بار مصرف (به ساعت)',
            'total_dosage': 'مقدار کل مصرف (گرم)',
            'dosage_every_time': 'مقدار هربار مصرف (گرم)',
            'starting_time': 'تاریخ شروع',
            'starting_hour': 'زمان شروع',
            'status': 'فعال بود یادآوری'
        }
        widgets = {
            'starting_time': forms.DateInput(attrs={'class': 'datepicker'}),
            'starting_hour': TimePickerInput(),

        }

    def clean(self):
        clean_med_date(self)
        if 'total_dosage' in self.cleaned_data.keys() and 'dosage_every_time' in self.cleaned_data.keys() \
                and self.cleaned_data['total_dosage'] and self.cleaned_data['dosage_every_time'] \
                and self.cleaned_data['dosage_every_time'] > self.cleaned_data['total_dosage']:
            if 'dosage_every_time' in self.errors.keys():
                self.errors['dosage_every_time'] += ['مقدار مصرف هر بار باید کوچکتر از مقدار مصرف کل باشد.']
            else:
                self.errors['dosage_every_time'] = ['مقدار مصرف هر بار باید کوچکتر از مقدار مصرف کل باشد.']

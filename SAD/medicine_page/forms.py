import datetime

from bootstrap_datepicker_plus import TimePickerInput
from django import forms
from django.utils.timezone import localtime, now

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

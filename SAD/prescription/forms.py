from django import forms
from django.core.exceptions import ValidationError
from jdatetime import datetime

from accounts.forms import DateInput
from .models import Tests, Medicine, Injections


class MedForm(forms.ModelForm):
    """
    Form for individual medicines
    """
    prefix = 'med'

    class Meta:
        model = Medicine
        fields = (
            'name', 'description', 'time_interval', 'dosage_every_time', 'total_dosage'
        )
        labels = {
            'name': 'نام',
            'description': 'توضیح',
            'time_interval': 'بازه زمانی بین دو بار مصرف (به ساعت)',
            'total_dosage': 'مقدار کل مصرف (گرم)',
            'dosage_every_time': 'مقدار هربار مصرف (گرم)'
        }

    def check_completeness(self):
        empty = False
        idx = []

        for i in range(int(self.data['med-TOTAL_FORMS'])):
            if not self.data['med-' + str(i) + '-name'] and not \
                    self.data['med-' + str(i) + '-description'] and not \
                    self.data['med-' + str(i) + '-time_interval'] and not \
                    self.data['med-' + str(i) + '-dosage_every_time'] and not \
                    self.data['med-' + str(i) + '-total_dosage']:
                empty = True
                idx += [i]
        return empty, idx

    def clean(self):
        errors = {'name': [], 'time_interval': [], 'total_dosage': [], 'dosage_every_time': []}
        cln = self.cleaned_data
        if 'name' not in cln.keys():
            errors['name'] += ['لطفا نام دارو را وارد کنید.']
        if 'time_interval' not in cln.keys():
            errors['time_interval'] += ['لطفا بازه زمانی را مشخص کنید.']
        if 'total_dosage' not in cln.keys():
            errors['total_dosage'] += ['لطفا مقدار کل مصرف را مشخص کنید.']
        if 'dosage_every_time' not in cln.keys():
            errors['dosage_every_time'] += ['لطفا مقدار هر بار مصرف را مشخص کنید.']
        if len(errors['name']) > 0 or len(errors['time_interval']) > 0 \
                or len(errors['dosage_every_time']) > 0 or len(errors['total_dosage']):
            raise ValidationError(errors)


class TestForm(forms.ModelForm):
    """
    Form for individual test
    """
    prefix = 'test'

    class Meta:
        model = Tests
        fields = (
            'name', 'description', 'deadline'
        )
        labels = {
            'name': 'نام',
            'description': 'توضیح',
            'deadline': 'مهلت انجام تا'
        }
        widgets = {
            'deadline': forms.DateInput(attrs={'class': 'datepicker'})
        }

    def check_completeness(self):
        empty = False
        idx = []

        for i in range(int(self.data['test-TOTAL_FORMS'])):
            if not self.data['test-' + str(i) + '-name'] and not \
                    self.data['test-' + str(i) + '-description'] and not \
                    self.data['test-' + str(i) + '-deadline']:
                empty = True
                idx += [i]
        return empty, idx

    def clean(self):
        errors = {'name': [], 'deadline': []}
        cln = self.cleaned_data
        if 'name' not in cln.keys():
            errors['name'] += ['لطفا نام دارو را وارد کنید.']
        if 'deadline' not in cln.keys():
            errors['deadline'] += ['لطفا تاریخ را وارد کنید.']
        if len(errors['name']) > 0 or len(errors['deadline']) > 0:
            raise ValidationError(errors)


class InjectionForm(forms.ModelForm):
    """
    Form for individual injection
    """
    prefix = 'injection'

    class Meta:
        model = Injections
        fields = (
            'name', 'description', 'deadline'
        )
        labels = {
            'name': 'نام',
            'description': 'توضیح',
            'deadline': 'مهلت انجام تا'
        }
        widgets = {
            'deadline': DateInput()
        }

    def check_completeness(self):
        empty = False
        idx = []
        for i in range(int(self.data['injection-TOTAL_FORMS'])):
            if not self.data['injection-' + str(i) + '-name'] and not \
                    self.data['injection-' + str(i) + '-description'] and not \
                    self.data['injection-' + str(i) + '-deadline']:
                empty = True
                idx += [i]
        return empty, idx

    def clean(self):
        errors = {'name': [], 'deadline': []}
        cln = self.cleaned_data
        date = cln['deadline']

        if 'name' not in cln.keys():
            errors['name'] += ['لطفا نام دارو را وارد کنید.']
        if 'deadline' not in cln.keys():
            errors['deadline'] += ['لطفا تاریخ را مشخص کنید.']
        if date < datetime.today().date().togregorian():
            errors['deadline'] += ['از این تاریخ گذشته است.']
        if len(errors['name']) > 0 or len(errors['deadline']) > 0:
            raise ValidationError(errors)

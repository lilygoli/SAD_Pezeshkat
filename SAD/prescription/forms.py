from django import forms
from django.core.exceptions import ValidationError

from .models import Tests, Medicine, Injections


class MedForm(forms.ModelForm):
    """
    Form for individual medicines
    """

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
        print("DDDD", self.data)
        empty = False
        idx = -1
        for i in range(int(self.data['form-TOTAL_FORMS'])):
            if not self.data['form-' + str(i) + '-name'] and not \
                    self.data['form-' + str(i) + '-description'] and not \
                    self.data['form-' + str(i) + '-time_interval'] and not \
                    self.data['form-' + str(i) + '-dosage_every_time'] and not \
                    self.data['form-' + str(i) + '-total_dosage']:
                empty = True
                idx = i
        return empty, idx

    def clean(self):
        errors = {'name': [], 'time_interval': [], 'total_dosage': [], 'dosage_every_time': []}
        cln = self.cleaned_data
        print("CLNNNN", cln)
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

    class Meta:
        model = Tests
        fields = (
            'name', 'description', 'deadline'
        )
        labels = {
            'name': 'نام',
            'description': 'توضیح',
            'deadline': 'تا تاریخ'
        }

    def check_completeness(self):
        empty = False
        idx = -1
        for i in range(int(self.data['form-TOTAL_FORMS'])):
            if not self.data['form-' + str(i) + '-name'] and not \
                    self.data['form-' + str(i) + '-description'] and not \
                    self.data['form-' + str(i) + '-deadline']:
                empty = True
                idx = i
        return empty, idx

    def clean(self):
        errors = {'name': [], 'deadline': []}
        cln = self.cleaned_data
        if 'name' not in cln.keys():
            errors['name'] += ['لطفا نام دارو را وارد کنید.']
        if 'deadline' not in cln.keys():
            errors['deadline'] += ['لطفا مقدار تاریخ را مشخص کنید.']
        if len(errors['name']) > 0 or len(errors['deadline']) > 0:
            raise ValidationError(errors)


class InjectionForm(forms.ModelForm):
    """
    Form for individual injection
    """

    class Meta:
        model = Injections
        fields = (
            'name', 'description', 'deadline'
        )
        labels = {
            'name': 'نام',
            'description': 'توضیح',
            'deadline': 'تا تاریخ'
        }

    def check_completeness(self):
        empty = False
        idx = -1
        for i in range(int(self.data['form-TOTAL_FORMS'])):
            if not self.data['form-' + str(i) + '-name'] and not \
                    self.data['form-' + str(i) + '-description'] and not \
                    self.data['form-' + str(i) + '-deadline']:
                empty = True
                idx = i
        return empty, idx

    def clean(self):
        errors = {'name': [], 'deadline': []}
        cln = self.cleaned_data
        if 'name' not in cln.keys():
            errors['name'] += ['لطفا نام دارو را وارد کنید.']
        if 'deadline' not in cln.keys():
            errors['deadline'] += ['لطفا مقدار تاریخ را مشخص کنید.']
        if len(errors['name']) > 0 or len(errors['deadline']) > 0:
            raise ValidationError(errors)

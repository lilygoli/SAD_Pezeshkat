from django import forms

from .models import Tests, Medicine, Injections


class MedForm(forms.ModelForm):
    """
    Form for individual medicines
    """

    class Meta:
        model = Medicine
        fields = (
            'name', 'description', 'time_interval', 'total_dosage', 'dosage_every_time'
        )



class TestFrom(forms.ModelForm):
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
            'deadline': 'مهلت انجام تا'
        }


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
            'deadline': 'مهلت انجام تا'
        }

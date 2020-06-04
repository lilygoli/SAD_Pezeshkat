from django.views.generic import ListView

from doctor_calendar.models import Event
from prescription.models import Tests, Injections, Medicine, Prescriptions
from django.shortcuts import redirect, render

class PrescriptionListPatientView(ListView):
    template_name = 'prescription_list_patient/pre_list_patient.html'
    prescrip = None
    medicine = None
    tests = None
    injections = None

    def get_queryset(self, ):
        self.prescrip = Prescriptions.objects.filter(patient=self.request.user.pk, doctor=self.kwargs['pk'])
        self.medicine = {}
        self.tests = {}
        self.injections = {}
        for i in self.prescrip:
            self.medicine.update({i: Medicine.objects.filter(prescription=i)})
            self.tests.update({i: Tests.objects.filter(prescription=i)})
            self.injections.update({i: Injections.objects.filter(prescription=i)})

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.GET.get('mySubmit'):
            pres = Prescriptions.objects.filter(comment=self.request.GET.get('tmp'))[0]
            print(pres.comment)
            pres.comment = self.request.GET.get('comment')
            pres.save()
            self.prescrip = Prescriptions.objects.filter(patient=self.request.user.pk, doctor=self.kwargs['pk'])
            # return render(self.request, 'prescription_list_patient/pre_list_patient.html', self.args)


        context = super().get_context_data(**kwargs)
        context['pre'] = self.prescrip
        context['medicine'] = self.medicine
        context['tests'] = self.tests
        context['injections'] = self.injections
        return context

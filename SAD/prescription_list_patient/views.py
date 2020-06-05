from django.views.generic import ListView

from doctor_calendar.models import Event
from prescription.models import Tests, Injections, Medicine, Prescriptions
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect


class PrescriptionListPatientView(ListView):
    template_name = 'prescription_list_patient/pre_list_patient.html'
    prescrip = None
    medicine = None
    tests = None
    injections = None

    def get_queryset(self, ):
        self.prescrip = Prescriptions.objects.filter(patient=self.request.user.pk, doctor=self.kwargs['pk']).order_by(
            'id')
        self.medicine = {}
        self.tests = {}
        self.injections = {}

        for i in self.prescrip:
            # print(len(Medicine.objects.filter(prescription=i)))
            if len(Medicine.objects.filter(prescription=i)) == 0 and len(Tests.objects.filter(
                    prescription=i)) == 0 and len(Injections.objects.filter(prescription=i)) == 0:
                self.prescrip = self.prescrip.exclude(id=i.id)
            self.medicine.update({i: Medicine.objects.filter(prescription=i)})
            self.tests.update({i: Tests.objects.filter(prescription=i)})
            self.injections.update({i: Injections.objects.filter(prescription=i)})

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.GET.get('mySubmit'):
            pres = Prescriptions.objects.filter(comment=self.request.GET.get('tmp'))[0]
            pres.comment = self.request.GET.get('comment')
            pres.save()
            self.prescrip = Prescriptions.objects.filter(patient=self.request.user.pk, doctor=self.kwargs['pk'])


        context = super().get_context_data(**kwargs)
        context['pre'] = self.prescrip
        context['medicine'] = self.medicine
        context['tests'] = self.tests
        context['injections'] = self.injections
        return context

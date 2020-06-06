from django.views.generic import ListView
from prescription.models import Tests, Injections, Medicine, Prescriptions


class PrescriptionListView(ListView):
    template_name = 'prescription_list/pre_list.html'
    prescrip = None
    medicine = {}
    tests = {}
    injections = {}

    def get_queryset(self, ):
        self.prescrip = Prescriptions.objects.filter(doctor=self.request.user.pk, patient=self.kwargs['pk']).order_by(
            'id')
        for i in self.prescrip:
            if len(Medicine.objects.filter(prescription=i)) == 0 and len(Tests.objects.filter(
                    prescription=i)) == 0 and len(Injections.objects.filter(prescription=i)) == 0:
                self.prescrip = self.prescrip.exclude(id=i.id)
            self.medicine.update({i: Medicine.objects.filter(prescription=i)})
            self.tests.update({i: Tests.objects.filter(prescription=i)})
            self.injections.update({i: Injections.objects.filter(prescription=i)})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pre'] = self.prescrip
        context['medicine'] = self.medicine
        context['tests'] = self.tests
        context['injections'] = self.injections
        return context

from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from .forms import MedForm, TestForm, InjectionForm
from prescription.models import Tests, Injections, Medicine, Prescriptions
from django.views.generic import ListView



@login_required
def make_prescription(request, doc_id, patient_id, event_id):
    p, _ = Prescriptions.objects.get_or_create(appointment_id=event_id, doctor_id=doc_id, patient_id=patient_id)
    return redirect('prescription:prescription', prescription_id=p.pk, cal=0)


@login_required
def write_prescription(request, **kwargs):
    prescription_id = kwargs['prescription_id']
    cal = kwargs['cal']
    # Create the formset, specifying the form and formset we want to use.
    MedFormSet = formset_factory(MedForm)
    TestFormSet = formset_factory(TestForm)
    InjectionFormSet = formset_factory(InjectionForm)

    # Get our existing link data for this user.  This is used as initial data.
    medicines = Medicine.objects.filter(prescription_id=prescription_id).order_by('id')
    tests = Tests.objects.filter(prescription_id=prescription_id).order_by('id')
    injections = Injections.objects.filter(prescription_id=prescription_id).order_by('id')
    medicine_list = [
        {'prescription_id': l.prescription_id, 'name': l.name, 'description': l.description,
         'time_interval': l.time_interval, 'total_dosage': l.total_dosage,
         "dosage_every_time": l.dosage_every_time}
        for l in medicines]
    test_list = [
        {'prescription_id': l.prescription_id, 'name': l.name, 'description': l.description, 'deadline': l.deadline}
        for l in tests]
    injection_list = [
        {'prescription_id': l.prescription_id, 'name': l.name, 'description': l.description, 'deadline': l.deadline}
        for l in injections]

    if request.method == 'POST':
        medicine_formset = MedFormSet(request.POST, prefix='med')
        test_formset = TestFormSet(request.POST, prefix='test')
        injection_formset = InjectionFormSet(request.POST, prefix='injection')

        # Now save the data for each form in the formset
        return_flag1 = make_item(request, medicine_formset, prescription_id, Medicine)
        return_flag2 = make_item(request, test_formset, prescription_id, Tests)
        return_flag3 = make_item(request, injection_formset, prescription_id, Injections)

        if return_flag1 and return_flag2 and return_flag3:
            if cal == '0':
                print('ok')
                return redirect('doctor_calendar:schedule', week_num=0)
            else:
                pk = Prescriptions.objects.filter(id=prescription_id)[0].patient_id
                return redirect('prescription:pre_list', pk=pk)

    else:

        medicine_formset = MedFormSet(initial=medicine_list, prefix='med')
        test_formset = TestFormSet(initial=test_list, prefix='test')
        injection_formset = InjectionFormSet(initial=injection_list, prefix='injection')

    context = {
        'medicine_formset': medicine_formset,
        'test_formset': test_formset,
        'injection_formset': injection_formset,

    }

    return render(request, 'prescription/prescription.html', context)


def make_item(request, medicine_formset, prescription_id, med_class):
    count = 0
    return_flag = True
    for med_form in medicine_formset:
        empty, idx = med_form.check_completeness()
        if not empty or count not in idx:
            if med_form.is_valid():
                m = med_form.save(commit=False)
                last_m = med_class.objects.filter(prescription_id=prescription_id, form_row=count)
                if len(last_m) <= 0:
                    m.prescription_id = prescription_id
                    m.form_row = count
                    if med_class == Medicine:
                        m.times_left = m.total_dosage // m.dosage_every_time + 1
                        m.dosage_remaining = m.total_dosage
                    m.save()
                else:
                    last_m = last_m[0]
                    last_m.name = m.name
                    last_m.description = m.description
                    if med_class == Medicine:
                        last_m.time_interval = m.time_interval
                        last_m.dosage_every_time = m.dosage_every_time
                        last_m.total_dosage = m.total_dosage
                        last_m.times_left = m.total_dosage // m.dosage_every_time + 1
                        last_m.dosage_remaining = m.total_dosage
                    else:
                        last_m.deadline = m.deadline
                    last_m.save()
            else:
                return_flag = False
                print(med_form.errors)
        count += 1
    return return_flag


def delete_med(request, med_id, prescription_id, cal, med_type):
    if med_type == '0':
        medication = Medicine
    elif med_type == '1':
        medication = Tests
    else:
        medication = Injections
    m = medication.objects.filter(prescription_id=prescription_id, form_row=med_id)

    if len(m):
        m[0].delete()
        ms = medication.objects.filter(prescription_id=prescription_id, form_row__gt=med_id)
        print(ms)
        for i in ms:
            i.form_row = i.form_row - 1
            i.save()
        return redirect('prescription:prescription', prescription_id=m[0].prescription_id, cal=cal)
    else:
        return redirect('prescription:prescription', prescription_id=prescription_id, cal=cal)


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
            self.prescrip = Prescriptions.objects.filter(patient=self.request.user.pk, doctor=self.kwargs['pk']).order_by('id')
            for i in self.prescrip:
                if len(Medicine.objects.filter(prescription=i)) == 0 and len(Tests.objects.filter(
                        prescription=i)) == 0 and len(Injections.objects.filter(prescription=i)) == 0:
                    self.prescrip = self.prescrip.exclude(id=i.id)

        context = super().get_context_data(**kwargs)
        context['pre'] = self.prescrip
        context['medicine'] = self.medicine
        context['tests'] = self.tests
        context['injections'] = self.injections
        return context

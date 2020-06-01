from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render

from .forms import MedForm, TestForm, InjectionForm
from .models import Medicine, Prescriptions, Tests, Injections


@login_required
def make_prescription(request, doc_id, patient_id, event_id):
    p, _ = Prescriptions.objects.get_or_create(appointment_id=event_id, doctor_id=doc_id, patient_id=patient_id)
    return redirect('prescription:prescription', prescription_id=p.pk)


@login_required
def write_prescription(request, **kwargs):
    prescription_id = kwargs['prescription_id']

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
        medicine_formset = MedFormSet(request.POST)
        # test_formset = TestFormSet(request.POST)
        # injection_formset = InjectionFormSet(request.POST)

        # Now save the data for each form in the formset
        count = 0
        return_flag = True
        for med_form in medicine_formset:
            empty, idx = med_form.check_completeness()
            print("Count", count)
            if med_form.is_valid():
                # print("chap", med_form)
                # print("validddd")
                if not empty or count != idx:
                    m = med_form.save(commit=False)
                    last_m = Medicine.objects.filter(prescription_id=prescription_id, form_row=count)
                    # print("lastm",last_m)
                    if len(last_m) <= 0:
                        m.prescription_id = prescription_id
                        m.form_row = count
                        m.save()
                    else:
                        last_m = last_m[0]
                        flag = False
                        if m.name != last_m.name:
                            last_m.name = m.name
                            flag = True
                        if m.description != last_m.description:
                            last_m.description = m.description
                            flag = True
                        if m.time_interval != last_m.time_interval:
                            last_m.time_interval = m.time_interval
                            flag = True
                        if m.dosage_every_time != last_m.dosage_every_time:
                            last_m.dosage_every_time = m.dosage_every_time
                            flag = True
                        if m.total_dosage != last_m.total_dosage:
                            last_m.total_dosage = m.total_dosage
                            flag = True
                        if flag:
                            last_m.save()

            else:
                return_flag = False
                print(med_form.errors)
            count += 1
        # for test_form in test_formset:
        #     if test_form.is_valid():
        #         t = test_form.save(commit=False)
        #         t.prescription_id = prescription_id
        #         t.save()
        #     else:
        #         print("testform")
        #         print(test_form.errors)
        # for injection_form in injection_formset:
        #     if injection_form.is_valid():
        #         i = injection_form.save()
        #         i.prescription_id = prescription_id
        #         i.save()
        #
        #     else:
        #         print("injection")
        #         print(injection_form.errors)
        if return_flag:
            return redirect('doctor_calendar:schedule', week_num=0)

    else:

        medicine_formset = MedFormSet(initial=medicine_list)
        test_formset = TestFormSet(initial=test_list)
        injection_formset = InjectionFormSet(initial=injection_list)

    context = {
        'medicine_formset': medicine_formset,
        # 'test_formset': test_formset,
        # 'injection_formset': injection_formset,
    }

    return render(request, 'prescription/prescription.html', context)


def delete_med(request, med_id, prescription_id):
    m = Medicine.objects.filter(prescription_id=prescription_id, form_row=med_id)
    if len(m):
        m[0].delete()
        ms = Medicine.objects.filter(prescription_id=prescription_id, form_row__gt=med_id)
        print(ms)
        for i in ms:
            i.form_row = i.form_row - 1
            i.save()
        return redirect('prescription:prescription', prescription_id=m[0].prescription_id)
    else:
        return redirect('prescription:prescription', prescription_id=prescription_id)


def delete_test(request, test_id, prescription_id):
    m = Tests.objects.filter(prescription_id=prescription_id, form_row=test_id)
    if len(m):
        m[0].delete()
        ms = Tests.objects.filter(prescription_id=prescription_id, form_row__gt=test_id)
        for i in ms:
            i.form_row = i.form_row - 1
            i.save()
        return redirect('prescription:prescription', prescription_id=m[0].prescription_id)
    else:
        return redirect('prescription:prescription', prescription_id=prescription_id)


def delete_injection(request, inj_id, prescription_id):
    m = Injections.objects.filter(prescription_id=prescription_id, form_row=inj_id)
    if len(m):
        m[0].delete()
        ms = Injections.objects.filter(prescription_id=prescription_id, form_row__gt=inj_id)
        for i in ms:
            i.form_row = i.form_row - 1
            i.save()
        return redirect('prescription:prescription', prescription_id=m[0].prescription_id)
    else:
        return redirect('prescription:prescription', prescription_id=prescription_id)

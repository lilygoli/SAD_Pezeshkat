from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render

from .forms import MedForm
from .models import Medicine, Prescriptions


@login_required
def make_prescription(request, doc_id, patient_id, event_id):
    p, _ = Prescriptions.objects.get_or_create(appointment_id=event_id, doctor_id=doc_id, patient_id=patient_id)
    return redirect('prescription:prescription', prescription_id=p.pk)


@login_required
def write_prescription(request, **kwargs):
    prescription_id = kwargs['prescription_id']

    # Create the formset, specifying the form and formset we want to use.
    MedFormSet = formset_factory(MedForm)

    # Get our existing link data for this user.  This is used as initial data.
    medicines = Medicine.objects.filter(prescription_id=prescription_id)
    medicine_list = [
        {'name': l.name, 'description': l.description, 'time_interval': l.time_interval, 'total_dosage': l.total_dosage,
         "dosage each time": l.dosage_every_time}
        for l in medicines]

    if request.method == 'POST':
        medicine_formset = MedFormSet(request.POST)

        # Now save the data for each form in the formset

        for med_form in medicine_formset:
            med_form.save()

    else:
        medicine_formset = MedFormSet(initial=medicine_list)

    context = {
        'medicine_formset': medicine_formset,
    }

    return render(request, 'prescription/prescription.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from prescription.models import Medicine
from .forms import StartMedFrom


class MedicineListView(ListView, FormMixin):
    template_name = 'medicine_page/medicine.html'
    meds = None

    def get_queryset(self):
        meds = Medicine.objects.filter(prescription__patient=self.request.user.pk)
        self.meds = meds
        return meds

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        self.meds.order_by('id')
        forms = [StartMedFrom() for i in range(len(self.meds))]
        zipped = zip(self.meds, forms)
        context['meds'] = zipped


        return context


@login_required
def set_start_time(request, med_id):
    if request.method == 'POST':
        med = Medicine.objects.get(id=med_id)
        prev_dosage = med.dosage_remaining
        prev_dosage_every = med.dosage_every_time
        med_form = StartMedFrom(request.POST, instance=med)
        if med_form.is_valid():
            m = med_form.save(commit=False)
            m.status = True
            if not m.dosage_remaining:
                m.dosage_remaining = prev_dosage
            if not m.dosage_every_time:
                m.dosage_every_time = prev_dosage_every
            m.save()
        else:
            all_meds = Medicine.objects.filter(prescription__patient=request.user.pk)
            med_form_list = []
            for i in all_meds:
                if i.id == int(med_id):
                    med_form_list += [med_form]
                else:
                    med_form_list += [StartMedFrom()]
            zipped = zip(all_meds,med_form_list)
            print(med_form.errors)
            print("INVALDDD")
            return render(request, 'medicine_page/medicine.html',
                          { 'meds': zipped, 'error_id': med_id})

    return redirect('medicine_page:medicines')


@login_required
def disable_notif(request, med_id):
    med = Medicine.objects.get(id=med_id)
    print(med, "RRRRRRRR")
    med.status = False
    med.save()

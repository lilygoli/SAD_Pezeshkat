from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from medicine_page.models import SelfAddedMedicine
from prescription.models import Medicine
from .forms import StartMedFrom, SelfMedForm, StartSelfMedFrom


class MedicineListView(ListView, FormMixin):
    template_name = 'medicine_page/medicine.html'
    meds = None
    self_meds = None

    def get_queryset(self):
        meds = Medicine.objects.filter(prescription__patient=self.request.user.pk).order_by('id')
        self_meds = SelfAddedMedicine.objects.filter(user=self.request.user).order_by('id')
        self.meds = meds
        self.self_meds = self_meds
        return meds, self_meds

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        self.meds.order_by('id')
        forms = [StartMedFrom() for i in range(len(self.meds))]
        self_forms = [StartSelfMedFrom() for i in range(len(self.self_meds))]
        zipped = zip(self.meds, forms)
        self_zipped = zip(self.self_meds, self_forms)
        empty_self_form = SelfMedForm()
        context['meds'] = zipped
        context['empty_self_form'] = empty_self_form
        context['self_meds'] = self_zipped

        return context


@login_required
def set_start_time(request, med_id, self):
    if request.method == 'POST':
        if self == '0':
            med = Medicine.objects.get(id=med_id)
            prev_dosage = med.dosage_remaining
            prev_dosage_every = med.dosage_every_time
            med_form = StartMedFrom(request.POST, instance=med)
        else:
            med = SelfAddedMedicine.objects.get(id=med_id)
            prev_dosage = med.dosage_remaining
            prev_dosage_every = med.dosage_every_time
            med_form = StartSelfMedFrom(request.POST, instance=med)
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
            self_meds = SelfAddedMedicine.objects.filter(user=request.user).order_by('id')
            self_forms = [StartSelfMedFrom() for i in range(len(self_meds))]

            med_form_list = []
            for i in all_meds:
                if i.id == int(med_id):
                    med_form_list += [med_form]
                else:
                    med_form_list += [StartMedFrom()]
            zipped = zip(all_meds, med_form_list)
            self_zipped = zip(self_meds, self_forms)
            print(med_form.errors)
            print("INVALDDD")
            return render(request, 'medicine_page/medicine.html',
                          {'meds': zipped, 'self_meds': self_zipped, 'error_id': med_id,
                           'empty_self_form': SelfMedForm()})

    return redirect('medicine_page:medicines')


@login_required
def disable_notif(request, med_id):
    med = Medicine.objects.get(id=med_id)
    print(med, "RRRRRRRR")
    med.status = False
    med.save()


@login_required
def disable_self_notif(request, med_id):
    med = SelfAddedMedicine.objects.get(id=med_id)
    med.status = False
    med.save()


@login_required
def add_med(request):
    if request.method == 'POST':
        med_form = SelfMedForm(request.POST)
        print(med_form)
        if med_form.is_valid():
            x = med_form.save(commit=False)
            x.user = request.user
            x.dosage_remaining = x.total_dosage
            x.save()
            print("xxxxxxxx", x)
        else:
            all_meds = Medicine.objects.filter(prescription__patient=request.user.pk)
            self_meds = SelfAddedMedicine.objects.filter(user=request.user).order_by('id')
            self_forms = [StartSelfMedFrom() for i in range(len(self_meds))]
            med_form_list = [StartSelfMedFrom() for i in range(len(all_meds))]
            zipped = zip(all_meds, med_form_list)
            self_zipped = zip(self_meds, self_forms)
            return render(request, 'medicine_page/medicine.html',
                          {'meds': zipped, 'self_meds': self_zipped, 'errors': med_form,
                           'empty_self_form': SelfMedForm()})

    return redirect('medicine_page:medicines')

# @login_required
# def write_prescription(request):
#     # Create the formset, specifying the form and formset we want to use.
#     MedFormSet = formset_factory(SelfMedForm)
#
#     # Get our existing link data for this user.  This is used as initial data.
#     medicines = SelfMedForm.objects.filter(user=request.user).order_by('id')
#
#     medicine_list = [
#         {'user': request.user, 'name': l.name, 'description': l.description,
#          'time_interval': l.time_interval, 'total_dosage': l.total_dosage,
#          "dosage_every_time": l.dosage_every_time, 'starting_time': l.starting_time,
#          'starting_hour': l.starting_hour}
#         for l in medicines]
#
#     if request.method == 'POST':
#         medicine_formset = MedFormSet(request.POST, prefix='self-med')
#
#         # Now save the data for each form in the formset
#         return_flag1 = make_item(request, medicine_formset)
#
#         if return_flag1:
#             return redirect('medicine_page:medicines')
#
#     else:
#
#         medicine_formset = MedFormSet(initial=medicine_list, prefix='med')
#
#     context = {
#         'medicine_formset': medicine_formset,
#
#     }
#
#     # return render(request, 'medicine_page/medicine.html',
#     #                       { 'meds': zipped, 'error_id': med_id})
#
#
# def make_item(request, medicine_formset):
#     count = 0
#     return_flag = True
#     for med_form in medicine_formset:
#         empty, idx = med_form.check_completeness()
#         if not empty or count not in idx:
#             if med_form.is_valid():
#                 m = med_form.save(commit=False)
#                 last_m = SelfMedForm.objects.filter(user_id=request.user.id, form_row=count)
#                 if len(last_m) <= 0:
#                     m.user = request.user
#                     m.times_left = m.total_dosage // m.dosage_every_time + 1
#                     m.dosage_remaining = m.total_dosage
#                     m.save()
#                 else:
#                     last_m = last_m[0]
#                     last_m.name = m.name
#                     last_m.description = m.description
#                     last_m.time_interval = m.time_interval
#                     last_m.dosage_every_time = m.dosage_every_time
#                     last_m.total_dosage = m.total_dosage
#                     last_m.times_left = m.total_dosage // m.dosage_every_time + 1
#                     last_m.dosage_remaining = m.total_dosage
#                     last_m.save()
#             else:
#                 return_flag = False
#                 print(med_form.errors)
#         count += 1
#     return return_flag

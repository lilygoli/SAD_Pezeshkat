import threading
import datetime
import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.utils.timezone import localtime, now
import jdatetime

from medicine_page.models import SelfAddedMedicine
from prescription.models import Medicine
from .forms import StartMedFrom, SelfMedForm, StartSelfMedFrom


class MedicineListView(ListView, FormMixin):
    template_name = 'medicine_page/medicine.html'
    meds = None
    self_meds = None

    def get_queryset(self):
        # print(self.request)
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
            print(request.POST)
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
            m.number += 1
            m.save()

            interval = datetime.datetime(m.starting_time.year, m.starting_time.month, m.starting_time.day, m.starting_hour.hour, m.starting_hour.minute,
                                         m.starting_hour.second) - jdatetime.datetime.now()
            # print("seconds ", request.user.email)
            t1 = threading.Thread(target=notify_me, args=(med_id, self, interval.seconds, request.user.email))
            t1.start()

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
            return render(request, 'medicine_page/medicine.html',
                          {'meds': zipped, 'self_meds': self_zipped, 'error_id': med_id,
                           'empty_self_form': SelfMedForm()})

    return redirect('medicine_page:medicines')


@login_required
def disable_notif(request, med_id):
    med = Medicine.objects.get(id=med_id)
    med.status = False
    med.send_notification = False
    med.save()

    return redirect('medicine_page:medicines')


@login_required
def disable_self_notif(request, med_id):
    med = SelfAddedMedicine.objects.get(id=med_id)
    med.status = False
    med.send_notification = False
    med.save()
    return redirect('medicine_page:medicines')


@login_required
def add_med(request):
    if request.method == 'POST':
        med_form = SelfMedForm(request.POST)
        print(med_form)
        if med_form.is_valid():
            x = med_form.save(commit=False)
            x.user = request.user
            x.dosage_remaining = x.total_dosage
            x.number += 1
            x.save()
            if x.status:
                interval = datetime.datetime(x.starting_time.year, x.starting_time.month, x.starting_time.day,
                                             x.starting_hour.hour, x.starting_hour.minute,
                                             x.starting_hour.second) - jdatetime.datetime.now()
                print("interval" , interval.seconds)

                t2 = threading.Thread(target=notify_me, args=(x.id, '1', interval.seconds, request.user.email))
                t2.start()
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


@login_required
def delete_med(request, med_id):
    SelfAddedMedicine.objects.filter(id=med_id).delete()
    return redirect('medicine_page:medicines')


def notify_me(med_id, type, seconds, email):
    med = None
    med_num = None
    if type == '0':
        med = Medicine.objects.get(id=med_id)
    else:
        med = SelfAddedMedicine.objects.get(id=med_id)
    med_num = med.number

    time.sleep(seconds)

    while True:
        if type == '0':
            med = Medicine.objects.get(id=med_id)
        else:
            med = SelfAddedMedicine.objects.get(id=med_id)

        if not med:
            return
        if med.finished or not med.status:
            med.send_notification = False
            med.save()
            break

        if med.number != med_num:
            med.send_notification = False
            med.save()
            break

        decrement_med(med_id, type)
        print("reminder ", "email sent")
        # send_mail(   'یاد آوری! ', 'قرص + med.name + 'فراموشی نشه ! ', 'admin@pezeshkat.com', [email], fail_silently=False, )
        time.sleep(1200)
        if type == '0':
            med = Medicine.objects.get(id=med_id)
        else:
            med = SelfAddedMedicine.objects.get(id=med_id)

        if med.number != med_num:
            break

        if not med:
            return
        med.send_notification = False
        med.save()
        print("remind 2")
        time.sleep(int(med.time_interval * 60 * 60) - 1200)


def decrement_med(med_id, type):
    if type == '0':  # for prescription medicine
        med = Medicine.objects.get(id=med_id)
    else:  # for self-added medicine
        med = SelfAddedMedicine.objects.get(id=med_id)
    if not med:
        return

    print("decrement")
    if med.dosage_remaining is None:
        med.dosage_remaining = med.total_dosage
    if med.dosage_remaining <= med.dosage_every_time:
        med.dosage_remaining = 0
        # med.times_left = 0
        med.status = False
        med.finished = True
    else:
        med.dosage_remaining -= med.dosage_every_time
        # med.times_left -= 1

    med.send_notification = True
    print("reached")
    med.save()

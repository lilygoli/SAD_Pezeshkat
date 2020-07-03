from datetime import datetime

import jdatetime
from django.db.models.functions import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime, now

from accounts.models import User
from doctor_calendar.models import Event
from medicine_page.models import SelfAddedMedicine
from prescription.models import Medicine, Prescriptions
from .forms import SelfMedForm, StartMedFrom, StartSelfMedFrom


class PrescriptionViewTestCase(TestCase):

    def set_up(self):
        pres = self.pre_set()
        med = Medicine.objects.create(prescription=pres, form_row=0, name='anti-human', time_interval=1,
                                      total_dosage=200, dosage_every_time=10)
        return med

    def pre_set(self):
        doc = User.objects.create_user(email='test@yahoo.com', password='testingtesting123', is_doctor=True,
                                       name='Test_doc',
                                       family_name='Test_family_doc')
        patient = User.objects.create_user(email='test_user@yahoo.com', password='testingtesting123', is_doctor=False,
                                           name='Test_user',
                                           family_name='Test_family_user')
        event = Event.objects.create(doctor_user=doc, patient_user=patient, start_hour=12,
                                     start_time=datetime.datetime(2020, 12, 1))
        pres = Prescriptions.objects.create(appointment_id=event.id, doctor_id=doc.id, patient_id=patient.id)
        return pres

    def test_medicine_list_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        User.objects.create_user(email='test@yahoo.com', password='testingtesting123', is_doctor=False,
                                 name='Test_user',
                                 family_name='Test_family_user')
        self.client.login(email='test@yahoo.com', password='testingtesting123')
        response = self.client.get(reverse('medicine_page:medicines'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'medicine_page/medicine.html')
        i = response.context['empty_self_form']
        self.failUnless(isinstance(i, SelfMedForm))

        for i in response.context['meds']:
            self.failUnless(isinstance(list(i)[0], Medicine))
            self.failUnless(isinstance(list(i)[1], StartMedFrom))

        for i in response.context['self_meds']:
            self.failUnless(isinstance(list(i)[0], SelfAddedMedicine))
            self.failUnless(isinstance(list(i)[1], StartSelfMedFrom))

    def test_start_notif_post(self):

        User.objects.create_user(email='test2@yahoo.com', password='testingtesting123', is_doctor=False,
                                 name='Test_user',
                                 family_name='Test_family_user')

        self.client.login(email='test2@yahoo.com', password='testingtesting123')
        med = self.set_up()
        from datetime import datetime, timedelta
        time = datetime.now() + timedelta(minutes=1)
        time_str = str(time)[11:16]

        date = localtime(now()).date()
        jdate = jdatetime.GregorianToJalali(date.year, date.month, date.day)
        jdate_str = str(jdate.jyear) + '-' + "%02d" % jdate.jmonth + '-' + "%02d" % jdate.jday
        data = {'med-starting_hour': time_str, 'med-starting_time': jdate_str}
        response = self.client.post(reverse('medicine_page:start_notif', args=(med.id, '0',)),
                                    data=data, follow=True)

        self.assertRedirects(response, reverse('medicine_page:medicines'))
        self.assertEqual(str(Medicine.objects.filter(id=med.id).get().starting_hour)[:5], time_str)
        self.assertEqual(Medicine.objects.filter(id=med.id).get().status, True)

        self.assertEqual(Medicine.objects.filter(id=med.id).get().starting_time,
                         jdatetime.date(jdate.jyear, jdate.jmonth, jdate.jday))

    def test_disable_notif_get(self):

        User.objects.create_user(email='test3@yahoo.com', password='testingtesting123', is_doctor=False,
                                 name='Test_user',
                                 family_name='Test_family_user')

        self.client.login(email='test3@yahoo.com', password='testingtesting123')
        med = self.set_up()
        response = self.client.post(reverse('medicine_page:disable-notif', args=(med.id,)), follow=True)
        self.assertRedirects(response, reverse('medicine_page:medicines'))

        self.assertEqual(Medicine.objects.filter(id=med.id).get().status, False)

    def test_add_med_post(self):

        User.objects.create_user(email='test4@yahoo.com', password='testingtesting123', is_doctor=False,
                                 name='Test_user',
                                 family_name='Test_family_user')

        self.client.login(email='test4@yahoo.com', password='testingtesting123')
        self.pre_set()
        from datetime import datetime, timedelta
        time = datetime.now() + timedelta(minutes=1)
        time_str = str(time)[11:16]

        date = localtime(now()).date()
        jdate = jdatetime.GregorianToJalali(date.year, date.month, date.day)
        jdate_str = str(jdate.jyear) + '-' + "%02d" % jdate.jmonth + '-' + "%02d" % jdate.jday
        data = {'self-med-name': 'anti-human2', 'self-med-total_dosage': 200, 'self-med-dosage_every_time': 10,
                'self-med-time_interval': 1, 'self-med-starting_hour': time_str, 'self-med-starting_time': jdate_str}
        response = self.client.post(reverse('medicine_page:add_med', ),
                                    data=data, follow=True)

        self.assertRedirects(response, reverse('medicine_page:medicines'))
        self.assertEqual(SelfAddedMedicine.objects.count(), 1)

    def test_start_notif_failure_post(self):
        User.objects.create_user(email='test6@yahoo.com', password='testingtesting123', is_doctor=False,
                                 name='Test_user',
                                 family_name='Test_family_user')

        self.client.login(email='test6@yahoo.com', password='testingtesting123')
        med = self.set_up()
        from datetime import datetime, timedelta
        time = datetime.now() - timedelta(minutes=1)
        time_str = str(time)[11:16]

        date = localtime(now()).date()
        jdate = jdatetime.GregorianToJalali(date.year, date.month, date.day)
        jdate_str = str(jdate.jyear) + '-' + "%02d" % jdate.jmonth + '-' + "%02d" % jdate.jday
        data = {'med-starting_hour': time_str, 'med-starting_time': jdate_str}
        response = self.client.post(reverse('medicine_page:start_notif', args=(med.id, '0',)),
                                    data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        for med, form in response.context['meds']:
            self.assertTrue('med-starting_hour' in form.errors[0])

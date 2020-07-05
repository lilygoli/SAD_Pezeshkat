from django.db.models.functions import datetime
from django.test import TestCase
from django.urls import reverse

from accounts.models import User, DoctorProfileInfo, PatientProfileInfo
from doctor_calendar.models import Event
from prescription.forms import MedForm, TestForm, InjectionForm
from prescription.models import Prescriptions, Medicine, Tests, Injections



class PrescriptionViewTestCase(TestCase):

    def set_up(self):
        doc = User.objects.create_user(email='test@yahoo.com', password='testingtesting123', is_doctor=True,
                                       name='Test_doc',
                                       family_name='Test_family_doc')
        patient = User.objects.create_user(email='test_user@yahoo.com', password='testingtesting123', is_doctor=False,
                                           name='Test_user',
                                           family_name='Test_family_user')
        doctor_profile = DoctorProfileInfo.objects.create(user=doc, fee=10, credit=100)
        event = Event.objects.create(doctor_user=doc, patient_user=patient, start_hour=12,
                                     start_time=datetime.datetime(2020, 12, 1))
        pres = Prescriptions.objects.create(appointment_id=event.id, doctor_id=doc.id, patient_id=patient.id)
        self.client.login(email='test@yahoo.com', password='testingtesting123')
        return pres, doc, patient, event

    def make_formset(self, right):
        data = {
            # management_form data
            'med-TOTAL_FORMS': '1',
            'med-INITIAL_FORMS': '0',
            'med-MIN_NUM_FORMS': '0',
            'med-MAX_NUM_FORMS': '1000',

            # First user data
            'med-0-name': 'xxx',
            'med-0-description': 'jjjj',
            'med-0-time_interval': '10',
            'med-0-dosage_every_time': '100',
            'med-0-total_dosage': '10000',

            'test-TOTAL_FORMS': '1',
            'test-INITIAL_FORMS': '0',
            'test-MIN_NUM_FORMS': '0',
            'test-MAX_NUM_FORMS': '1000',
            'test-0-name': 'test1',
            'test-0-description': 'test',
            'test-0-deadline': '2020-12-01',

            'injection-TOTAL_FORMS': '1',
            'injection-INITIAL_FORMS': '0',
            'injection-MIN_NUM_FORMS': '0',
            'injection-MAX_NUM_FORMS': '1000',
            'injection-0-name': 'inject1',
            'injection-0-description': 'inject',

        }
        if right:
            data['injection-0-deadline'] = '2020-12-01'
        return data

    def test_prescription_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        pres, _, _, _ = self.set_up()
        response = self.client.get(reverse('prescription:prescription', args=(pres.id, 0,)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'prescription/prescription.html')
        for i in response.context['medicine_formset']:
            self.failUnless(isinstance(i, MedForm))

        for i in response.context['injection_formset']:
            self.failUnless(isinstance(i, InjectionForm))

        for i in response.context['test_formset']:
            self.failUnless(isinstance(i, TestForm))

    def test_prescription_view_post(self):

        data = self.make_formset(True)
        pres, _, _, _ = self.set_up()
        response = self.client.post(reverse('prescription:prescription', args=(pres.id, 0,)),
                                    data=data, follow=True)

        self.assertRedirects(response, reverse('doctor_calendar:schedule', args=(0,)))
        self.assertEqual(Medicine.objects.count(), 1)
        self.assertEqual(Tests.objects.count(), 1)
        self.assertEqual(Injections.objects.count(), 1)

    def test_prescription_view_failure(self):
        data = self.make_formset(False)
        pres, _, _, _ = self.set_up()
        response = self.client.post(reverse('prescription:prescription', args=(pres.id, 0,)),
                                    data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('deadline' in response.context['injection_formset'].errors[0])

    def test_make_prescription_view(self):
        _, doc, patient, event = self.set_up()
        patient2 = User.objects.create_user(email='test_user2@yahoo.com', password='testingtesting123', is_doctor=False,
                                            name='Test_user',
                                            family_name='Test_family_user')
        response = self.client.post(reverse('prescription:make-prescription', args=(doc.id, patient2.id, event.id)),
                                    follow=True)
        self.assertEqual(Prescriptions.objects.count(), 2)
        p = Prescriptions.objects.filter(doctor_id=doc.id, patient_id=patient2.id, appointment_id=event.id)[0]
        self.assertRedirects(response, reverse('prescription:prescription', args=(p.id, 0,)))


class DoctorPrescriptionTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(email='doctor@gmail.com', password='doc12345', is_doctor=True,
                                              name="doctor")
        test_user1_profile = DoctorProfileInfo.objects.create(user=test_user1, specialty="jarah", user_id=1,
                                                              address="blah")
        test_user1.save()
        test_user1_profile.save()

        test_user2 = User.objects.create_user(email='patient@gmail.com', is_doctor=False, name="patient",
                                              password='patient1234')
        test_user2_profile = PatientProfileInfo.objects.create(user=test_user2, user_id=2, birthday='2010-10-10',
                                                               medical_emergency_contact="09121211212")
        test_user2.save()
        test_user2_profile.save()

        test_event1 = Event.objects.create(doctor_user=test_user1, patient_user=test_user2, start_time='2020-10-10',
                                           start_hour=10)
        test_event1.save()

        prescription1 = Prescriptions.objects.create(doctor=test_user1, patient=test_user2, appointment=test_event1)
        prescription1.save()

        medicine1 = Medicine.objects.create(prescription=prescription1, form_row=1, name='med1', time_interval=1.5,
                                            total_dosage=10, dosage_every_time=1)
        medicine1.save()

        test1 = Tests.objects.create(prescription=prescription1, form_row=2, name="test1", deadline='1399-10-10')
        test1.save()

        injection1 = Injections.objects.create(prescription=prescription1, form_row=3, name="inj1",
                                               deadline='1399-10-10')
        injection1.save()

    def test_prescription_list(self):
        url = '{url}'.format(
            url=reverse('prescription:pre_list', args=[2]))
        self.client.login(username='doctor@gmail.com', password='doc12345')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['pre'], Prescriptions.objects.all(), transform=lambda x: x,
                                 ordered=False)
        self.assertQuerysetEqual(response.context['medicine'][response.context['pre'][0]], Medicine.objects.all(),
                                 transform=lambda x: x, ordered=False)
        self.assertQuerysetEqual(response.context['tests'][response.context['pre'][0]], Tests.objects.all(),
                                 transform=lambda x: x, ordered=False)
        self.assertQuerysetEqual(response.context['injections'][response.context['pre'][0]], Injections.objects.all(),
                                 transform=lambda x: x, ordered=False)


class PatientPrescriptionTest(TestCase):

    def setUp(self):
        DoctorPrescriptionTest.setUp(self)

    def test_prescription_list(self):
        url = '{url}'.format(
            url=reverse('prescription:pre_list_patient', args=[1]))
        self.client.login(username='patient@gmail.com', password='patient1234')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['pre'], Prescriptions.objects.all(), transform=lambda x: x,
                                 ordered=False)
        self.assertQuerysetEqual(response.context['medicine'][response.context['pre'][0]], Medicine.objects.all(),
                                 transform=lambda x: x, ordered=False)
        self.assertQuerysetEqual(response.context['tests'][response.context['pre'][0]], Tests.objects.all(),
                                 transform=lambda x: x, ordered=False)
        self.assertQuerysetEqual(response.context['injections'][response.context['pre'][0]], Injections.objects.all(),
                                 transform=lambda x: x, ordered=False)

from django.db.models.functions import datetime
from django.test import TestCase
from django.urls import reverse

from accounts.models import User, DoctorProfileInfo
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

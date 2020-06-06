from django.test import TestCase
from django.urls import reverse

from accounts.models import User, DoctorProfileInfo, PatientProfileInfo
from doctor_calendar.models import Event
from prescription.models import Prescriptions, Medicine, Tests, Injections


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
            url=reverse('prescription_list:pre_list', args=[2]))
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

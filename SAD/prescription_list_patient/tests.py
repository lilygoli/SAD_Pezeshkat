from django.test import TestCase
from django.urls import reverse
from prescription.models import Prescriptions, Medicine, Tests, Injections
from prescription_list.tests import DoctorPrescriptionTest


class PatientPrescriptionTest(TestCase):

    def setUp(self):
        DoctorPrescriptionTest.setUp(self)

    def test_prescription_list(self):
        url = '{url}'.format(
            url=reverse('prescription_list_patient:pre_list_patient', args=[1]))
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

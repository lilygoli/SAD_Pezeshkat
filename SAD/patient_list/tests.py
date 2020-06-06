from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from accounts.models import User, DoctorProfileInfo, PatientProfileInfo
from doctor_calendar.models import Event


class PatientListTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(email='aliii@gmail.com', password='ali12345', is_doctor=True,
                                              name="hasan")
        test_user1_profile = DoctorProfileInfo.objects.create(user=test_user1,specialty="jarah", user_id=1,
                                                              address="blah")
        test_user1.save()
        test_user1_profile.save()

        test_user2 = User.objects.create_user(email='hasan@gmail.com', is_doctor=False, name="hasan",
                                              password='hasan1234')
        test_user2_profile = PatientProfileInfo.objects.create(user=test_user2, user_id=2, birthday='2010-10-10',
                                                               medical_emergency_contact="09121211212")
        test_user2.save()
        test_user2_profile.save()

        test_event1 = Event.objects.create(doctor_user=test_user1, patient_user=test_user2, start_time='2020-10-10',
                                          start_hour=10)
        test_event1.save()

        test_user3 = User.objects.create_user(email='feri@gmail.com', is_doctor=False, name="feri",
                                              password='feri1234')
        test_user3_profile = PatientProfileInfo.objects.create(user=test_user3, user_id=3, birthday='2010-10-10',
                                                               medical_emergency_contact="09121211213")
        test_user3.save()
        test_user3_profile.save()

        test_event2 = Event.objects.create(doctor_user=test_user1, patient_user=test_user3, start_time='2020-10-10',
                                          start_hour=10)
        test_event2.save()

    def test_list(self):
        url = '{url}'.format(
            url=reverse('patient_list:list'))
        self.client.login(username='aliii@gmail.com', password='ali12345')
        response = self.client.get(url)
        print(response.context['patients'])
        print(PatientProfileInfo.objects.all().order_by('id'))
        self.assertQuerysetEqual(response.context['patients'], PatientProfileInfo.objects.all(), transform=lambda x: x,
                                 ordered=False)




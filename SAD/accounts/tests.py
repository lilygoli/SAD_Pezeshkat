from accounts import forms
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, DoctorProfileInfo, PatientProfileInfo
from doctor_calendar.models import Event


class RegistrationViewTestCase(TestCase):

    def test_registration_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response,
                                'registration/registration.html')
        self.failUnless(isinstance(response.context['user_form'],
                                   forms.UserForm))

        self.failUnless(isinstance(response.context['profile_form'],
                                   forms.DoctorProfileInfoForm) or isinstance(response.context['profile_form'],
                                                                              forms.PatientProfileInfoFrom))

    def test_registration_view_post_success(self):
        """
        A ``POST`` to the ``register`` view with valid data properly
        creates a new user and issues a redirect.

        """
        response = self.client.post(reverse('accounts:register'),
                                    data={'name': 'ali',
                                          'family_name': 'baghayi',
                                          'email': 'aliThePerfect@yahoo.com',
                                          'password': '55588l',
                                          'birthday': '1377-12-12',
                                          'medical_emergency_contact': '09121026857',
                                          }, follow=True)

        self.assertRedirects(response, reverse('user_login'))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(PatientProfileInfo.objects.count(), 1)

    def test_registration_view_post_failure(self):
        """
        A ``POST`` to the ``register`` view with invalid data does not
        create a user, and displays appropriate error messages.

        """
        response = self.client.post(reverse('accounts:register'),
                                    data={'name': 'ali',
                                          'family_name': 'baghayi',
                                          'email': 'aliThePerfectMan@yahoo.com',
                                          'password': '5558888',
                                          'birthday': '1377-12-12',
                                          'medical_emergency_contact': '09121026857',
                                          }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('رمز عبور باید دارای حداقل یک عدد و یک کاراکتر الفبا باشد.' in response.context['errors'])


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
            url=reverse('accounts:list'))
        self.client.login(username='aliii@gmail.com', password='ali12345')
        response = self.client.get(url)
        print(response.context['patients'])
        print(PatientProfileInfo.objects.all().order_by('id'))
        self.assertQuerysetEqual(response.context['patients'], PatientProfileInfo.objects.all(), transform=lambda x: x,
                                 ordered=False)




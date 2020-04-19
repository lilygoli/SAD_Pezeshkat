from django.test import TestCase
from django.urls import reverse

from accounts import forms
from accounts.models import User, PatientProfileInfo


class RegistrationViewTestCase(TestCase):


    def test_registration_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        response = self.client.get(reverse('register'))
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
        response = self.client.post(reverse('register'),
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
        response = self.client.post(reverse('register'),
                                    data={'name': 'ali',
                                          'family_name': 'baghayi',
                                          'email': 'aliThePerfectMan@yahoo.com',
                                          'password': '5558888',
                                          'birthday': '1377-12-12',
                                          'medical_emergency_contact': '09121026857',
                                          }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('رمز عبور باید دارای حداقل یک عدد و یک کاراکتر الفبا باشد.' in response.context['errors'])




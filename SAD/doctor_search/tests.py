from django.test import TestCase
from accounts.models import DoctorProfileInfo
from accounts.models import User


# from SAD.accounts.models import DoctorProfileInfo
# from SAD.accounts.models import User

class DoctorSearchTest(TestCase):
    def setUp(self):
        DoctorProfileInfo.objects.create(specialty="jarah", user_id=1,
                                         user=User.objects.create(name="ali", is_doctor=True, email='ali@gmail.com'))
        DoctorProfileInfo.objects.create(specialty="goosh", user_id=2,
                                         user=User.objects.create(name="mohammad", is_doctor=True, email='mohammad@gmail.com'))

    def test_doctor_search(self):
        doc1 = DoctorProfileInfo.objects.get(specialty__contains="ja")
        doc2 = DoctorProfileInfo.objects.get(specialty__contains="sh")
        self.assertEqual(doc1.specialty, 'jarah')
        self.assertNotEqual(doc2.user.name, 'ali')

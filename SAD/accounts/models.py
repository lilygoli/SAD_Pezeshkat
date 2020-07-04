# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=False)
    family_name = models.CharField(max_length=254, null=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_doctor = models.BooleanField(null=False)
    bank = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['is_doctor']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class DoctorProfileInfo(models.Model):
    PHD = 'دکتری'
    BACHELOR = 'کارشناسی'
    MASTER = 'کارشناسی‌ارشد'
    SPECIALIST = 'تخصص'
    SUPER_SPECIALIST = 'فوق‌تخصص'
    NORMAL = '-'
    DOCTOR_CHOICES = (
        (PHD, 'دکتری'),
        (BACHELOR, 'کارشناسی'),
        (MASTER, 'کارشناسی ارشد'),
        (SPECIALIST, 'تخصص'),
        (SUPER_SPECIALIST, 'فوق تخصص'),
        (NORMAL, '-')
    )

    EYE = 'ﭼﺸﻢ ﭘﺰﺷﮑﯽ'
    RADIO = 'ﺭﺍﺩﯾﻮﻟﻮﮊﯼ'
    SKIN = 'ﭘﻮﺳﺖ ﻭ ﻣﻮ'
    NUCLEAR = "ﭘﺰﺷﮑﯽﻫﺴﺘﻪﺍﯼ"
    PEDI = "ﺍﺭﺗﻮﭘﺪﯼ"
    CARDIO = 'ﻗﻠﺐﻭﻋﺮﻭﻕ'
    PHYIS = 'ﻃﺐ ﻓﯿﺰﯾﮑﯽ'
    NEURO = 'ﻣﻐﺰﻭﺍﻋﺼﺎﺏ'
    EAR = 'ﮔﻮﺵ ﺣﻠﻖ ﺑﯿﻨﯽ'
    MELENDEZ_HON = 'ﺟﺮﺍﺣﯽ ﻣﻐﺰﻭﺍﻋﺼﺎﺏ'
    PATH = 'ﭘﺎﺗﻮﻟﻮﮊﯼ'
    URO = 'ﮐﻠﯿﻪ ﻭ ﻣﺠﺎﺭﯼﺍﺩﺭﺍﺭﯼ'
    RAY = 'ﭘﺮﺗﻮﺩﺭﻣﺎﻧﯽ - ﺭﺍﺩﯾﻮﺗﺮﺍﭘﯽ'
    BUZARI = 'ﺟﺮﺍﺣﯽ ﻋﻤﻮﻣﯽ'
    WOMEN = 'ﺯﻧﺎﻥ ﻭ ﺯﺍﯾﻤﺎﻥ'
    PSYCH = 'ﺭﻭﺍﻧﭙﺰﺷﮑﯽ'
    INTERNAL = 'ﺩﺍﺧﻠﯽ'
    WORK = 'ﻃﺐﮐﺎﺭ'
    KIDS = 'ﮐﻮﺩﮐﺎﻥ'
    ANSTH = 'ﺑﯿﻬﻮﺷﯽ'
    INFECT = 'ﻋﻔﻮﻧﯽ'
    NONE = '-'
    SPCIALTY_CHOICES = (
        (EYE, 'ﭼﺸﻢ ﭘﺰﺷﮑﯽ'),
        (RADIO, 'ﺭﺍﺩﯾﻮﻟﻮﮊﯼ'),
        (SKIN, 'ﭘﻮﺳﺖ ﻭ ﻣﻮ'),
        (NUCLEAR, "ﭘﺰﺷﮑﯽﻫﺴﺘﻪﺍﯼ"),
        (PEDI, "ﺍﺭﺗﻮﭘﺪﯼ"),
        (CARDIO, 'ﻗﻠﺐﻭﻋﺮﻭﻕ'),
        (PHYIS, 'ﻃﺐ ﻓﯿﺰﯾﮑﯽ'),
        (NEURO, 'ﻣﻐﺰﻭﺍﻋﺼﺎﺏ'),
        (EAR, 'ﮔﻮﺵ ﺣﻠﻖ ﺑﯿﻨﯽ'),
        (MELENDEZ_HON, 'ﺟﺮﺍﺣﯽ ﻣﻐﺰﻭﺍﻋﺼﺎﺏ'),
        (PATH, 'ﭘﺎﺗﻮﻟﻮﮊﯼ'),
        (URO, 'ﮐﻠﯿﻪ ﻭ ﻣﺠﺎﺭﯼﺍﺩﺭﺍﺭﯼ'),
        (RAY, 'ﭘﺮﺗﻮﺩﺭﻣﺎﻧﯽ - ﺭﺍﺩﯾﻮﺗﺮﺍﭘﯽ'),
        (BUZARI, 'ﺟﺮﺍﺣﯽ ﻋﻤﻮﻣﯽ'),
        (WOMEN, 'ﺯﻧﺎﻥ ﻭ ﺯﺍﯾﻤﺎﻥ'),
        (PSYCH, 'روانپزشکی'),
        (INTERNAL, 'ﺩﺍﺧﻠﯽ'),
        (WORK, 'ﻃﺐﮐﺎﺭ'),
        (KIDS, 'ﮐﻮﺩﮐﺎﻥ'),
        (ANSTH, 'ﺑﯿﻬﻮﺷﯽ'),
        (INFECT, 'ﻋﻔﻮﻧﯽ'),
        (NONE, '-')

    )
    ONE_HOUR, HALF_HOUR, THREE_QUARTER = 1, 0.5, 0.75
    DURATIONS = ((ONE_HOUR, 'یک ساعت'), (HALF_HOUR, 'نیم ساعت'), (THREE_QUARTER, 'سه ربع'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default=None)
    specialty_bins = models.CharField(max_length=254, null=False, choices=SPCIALTY_CHOICES, default=NONE)
    specialty = models.CharField(max_length=254, null=True, blank=True)
    degree = models.CharField(max_length=254, null=True, choices=DOCTOR_CHOICES, default=NORMAL)
    educational_background = models.CharField(max_length=254, null=True, blank=True)
    score = models.FloatField(blank=True, null=True, default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    fee = models.FloatField(blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    on_site_fee = models.BooleanField(blank=True, default=False)
    address = models.CharField(max_length=500, null=False)
    credit = models.FloatField(blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    visit_duration = models.FloatField(default=0.5, choices=DURATIONS)
    available_weekdays = models.CharField(max_length=8, default='1111100')
    start_hour = models.IntegerField(default=8, validators=[MaxValueValidator(20), MinValueValidator(8)])
    end_hour = models.IntegerField(default=20, validators=[MaxValueValidator(20), MinValueValidator(9)])

    def __str__(self):
        return self.user.name + ' ' + self.user.family_name


class PatientProfileInfo(models.Model):
    A = 'A'
    B = 'B'
    C = 'AB'
    D = 'O'
    M = 'M'
    P = 'P'
    BLOOD_TYPE = (
        (A, 'A'),
        (B, 'B'),
        (C, 'AB'),
        (D, 'O'),
    )
    BLOOD_PLUS_MINUS = (
        (M, '-'),
        (P, '+')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default=None)
    birthday = models.DateField(null=False)
    medical_condition = models.CharField(max_length=254, null=True, blank=True)
    credit = models.FloatField(blank=True, null=True, default=0, validators=[MinValueValidator(0)])
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    blood_type = models.CharField(max_length=4, null=True, choices=BLOOD_TYPE, blank=True)
    blood_plus_minus = models.CharField(max_length=2, null=True, choices=BLOOD_PLUS_MINUS, blank=True)
    allergies = models.CharField(max_length=254, null=True, blank=True)
    medical_emergency_contact = models.CharField(max_length=13, null=False,
                                                 error_messages={'شماره وارد شده معتبر نیست.': 'incomplete'},
                                                 validators=[RegexValidator(r'^[0]?9[0-9]{9}$',
                                                                            'شماره موبایل معتبر وارد کنید.')])

    def __str__(self):
        return self.user.name + ' ' + self.user.family_name


class Income(models.Model):
    start_date = jmodels.jDateField(null=False)
    end_date = jmodels.jDateField(null=False)

import datetime

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import EditProfileForm, PatientEditProfileInfo, DoctorEditProfileInfo, Inverse, TimeInterval
from accounts.forms import UserForm, PatientProfileInfoFrom, DoctorProfileInfoForm
from accounts.models import DoctorProfileInfo, User
from doctor_calendar.models import Event




def index(request):
    user = request.user
    if not user.is_authenticated:
        categories = DoctorProfileInfo.objects.order_by('specialty_bins').values(
            'specialty_bins'
        ).annotate(count=Count('specialty_bins'))
        counts_by_category = {Inverse[i['specialty_bins']]: i['count'] for i in categories}
        for i in Inverse.values():
            try:
                s = counts_by_category[i]
            except Exception:
                counts_by_category[i] = 0
        print(counts_by_category)
        args = counts_by_category
        return render(request, 'registration/index.html', args)
    else:

        args = {'user': user}
        if user.is_doctor:
            args.update({"days": get_week_days(user)})
            return render(request, 'registration/doctor_profile.html', args)
        else:
            return render(request, 'registration/patient_profile.html', args)


def get_week_days(user):
    work_days = ""
    doctor_days = user.doctorprofileinfo.available_weekdays
    week = {0: "شنبه", 1: "یک‌‌شنبه", 2: "دوشنبه", 3: "سه‌شنبه", 4: "چهار‌شنبه", 5: "پنج‌شنبه", 6: "جمعه"}
    for i in range(len(doctor_days)):
        if doctor_days[i] == '1':
            if work_days == "":
                work_days += week.get(i)
            else:
                work_days += "، " + week.get(i)
    return work_days


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:index'))


def register(request):
    errors = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        id = request.GET.get('id')
        if id == '1':
            profile_form = DoctorProfileInfoForm(data=request.POST)
        else:
            profile_form = PatientProfileInfoFrom(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            new_user = authenticate(username=user_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect(reverse('accounts:index'))
        else:

            for i in user_form.errors.values():
                errors += i + '\n'
            for j in profile_form.errors.values():
                errors += j + '\n'
            errors.pop()
            if id == '1':
                profile_form.fields['score'].widget = forms.HiddenInput()
                profile_form.fields['available_weekdays'].widget = forms.HiddenInput()

            user_form.fields['is_doctor'].widget = forms.HiddenInput()
            return render(request, 'registration/registration.html',
                          {'errors': errors, 'user_form': user_form, 'profile_form': profile_form})

    else:
        id = request.GET.get('id')
        print(id)
        if id == '1':
            user_form = UserForm(initial={'is_doctor': True})
            profile_form = DoctorProfileInfoForm(initial={'score': 0})
            profile_form.fields['score'].widget = forms.HiddenInput()
            profile_form.fields['available_weekdays'].widget = forms.HiddenInput()
        else:
            user_form = UserForm(initial={'is_doctor': False})
            profile_form = PatientProfileInfoFrom()
        user_form.fields['is_doctor'].widget = forms.HiddenInput()
    return render(request, 'registration/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form
                   })


def user_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('accounts:index'))
            else:
                error = "اکانت شما فعال نیست."
                return render(request, 'registration/login.html', {"error": error})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(email, password))
            error = "ایمیل یا رمز عبور اشتباه میباشد."
            return render(request, 'registration/login.html', {"error": error})
    else:
        return render(request, 'registration/login.html', {"error": error})


def edit_profile(request):
    if request.method == 'POST':
        edituser_form = EditProfileForm(request.POST, instance=request.user)
        if not request.user.is_doctor:
            editprofileinfo_form = PatientEditProfileInfo(request.POST, instance=request.user.patientprofileinfo)
        else:
            editprofileinfo_form = DoctorEditProfileInfo(request.POST, instance=request.user.doctorprofileinfo)
        if edituser_form.is_valid() and editprofileinfo_form.is_valid():
            user = edituser_form.save()
            profile = editprofileinfo_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            if not profile.profile_pic:
                profile.profile_pic = 'default.jpg'
            profile.save()
            return redirect(reverse('accounts:index'))
        else:
            print(edituser_form.errors, editprofileinfo_form.errors)
    else:
        edituser_form = EditProfileForm(instance=request.user)
        if not request.user.is_doctor:
            editprofileinfo_form = PatientEditProfileInfo(instance=request.user.patientprofileinfo)
        else:
            init = []
            weekdays = request.user.doctorprofileinfo.available_weekdays
            for i in range(7):
                if weekdays[i] == '1':
                    init.append(str(i))

            editprofileinfo_form = DoctorEditProfileInfo(instance=request.user.doctorprofileinfo,
                                initial={'available_weekdays': init})
        args = {'edituser_form': edituser_form, 'editprofileinfo_form': editprofileinfo_form}
        return render(request, 'registration/edit_profile.html', args)


@login_required
def mini_profile(request, pk):
    user_2 = User.objects.get(pk=pk)
    args = {'user': user_2, 'request_user': request.user}
    if user_2.is_doctor:
        args.update({"days": get_week_days(user_2)})
        return render(request, 'registration/doctor_mini_profile.html', args)
    else:
        return render(request, 'registration/patient_mini_profile.html', args)


@login_required
def monthly_income(request):
    doctor_fee = request.user.doctorprofileinfo.fee
    errors = ''
    if request.method == "POST":
        date_form = TimeInterval(request.POST)
        if date_form.is_valid():
            clean_data = date_form.cleaned_data
            appointments = Event.objects.filter(doctor_user=request.user)
            interval = clean_data['end_date'] - clean_data['start_date']
            income = {i: 0 for i in range(interval.days)}
            for i in appointments:
                if clean_data['start_date'].year == i.start_time.year:
                    if clean_data['start_date'].month <= i.start_time.month <= clean_data['end_date'].month:
                        if clean_data['start_date'].day <= i.start_time.day <= clean_data['end_date'].day:
                            day_diff = i.start_time.day - clean_data['start_date'].day
                            income.update({day_diff: income.get(day_diff) + doctor_fee})
            ins = [0]
            for i in range(interval.days):
                ins.append((ins[-1] + income.get(i)))
            ins.pop(0)
            args = {'form': date_form, 'income': income, 'ins': ins, 'errors':errors}
            return render(request, 'doctor_income/income.html', args)
        else:
            for i in date_form.errors.values():
                errors += i + '\n'
            errors.pop()
            args = {'form': date_form, 'income': {}, 'ins': {}, 'errors': errors}
            return render(request, 'doctor_income/income.html', args)
    else:
        date_form = TimeInterval()
        args = {'form': date_form, 'income': {}}
        return render(request, 'doctor_income/income.html', args)


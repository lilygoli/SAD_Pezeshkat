from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import EditProfileForm, PatientEditProfileInfo, DoctorEditProfileInfo, Inverse
from accounts.forms import UserForm, PatientProfileInfoFrom, DoctorProfileInfoForm
from accounts.models import DoctorProfileInfo, User


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
            return render(request, 'registration/doctor_profile.html', args)
        else:
            return render(request, 'registration/patient_profile.html', args)


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
            return HttpResponseRedirect(reverse('accounts:user_login'))
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
            editprofileinfo_form = DoctorEditProfileInfo(instance=request.user.doctorprofileinfo)
        args = {'edituser_form': edituser_form, 'editprofileinfo_form': editprofileinfo_form}
        return render(request, 'registration/edit_profile.html', args)


def mini_profile(request, pk):
    user_2 = User.objects.get(pk=pk)
    args = {'user': user_2}
    if user_2.is_doctor:
        return render(request, 'registration/doctor_mini_profile.html', args)
    else:
        return render(request, 'registration/patient_mini_profile.html', args)

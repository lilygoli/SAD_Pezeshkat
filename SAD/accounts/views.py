import os

from django import forms
from django.shortcuts import render, redirect
from accounts.forms import UserForm, PatientProfileInfoFrom, DoctorProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from accounts.forms import EditProfileForm, PatientEditProfileInfo


def index(request):
    user = request.user
    if not user.is_active:
        args = {}
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
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
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
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        id = request.GET.get('id')
        print(id)
        if id == '1':
            user_form = UserForm(initial={'is_doctor': True})
            profile_form = DoctorProfileInfoForm()
        else:
            user_form = UserForm(initial={'is_doctor': False})
            profile_form = PatientProfileInfoFrom()
        user_form.fields['is_doctor'].widget = forms.HiddenInput()
    return render(request, 'registration/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")  # TODO improve
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(email, password))
            return HttpResponse("Invalid login details given")  # TODO improve
    else:
        return render(request, 'registration/login.html', {})


def edit_profile(request):
    if request.method == 'POST':
        edituser_form = EditProfileForm(request.POST, instance=request.user)
        if not request.user.is_doctor:
            editprofileinfo_form = PatientEditProfileInfo(request.POST, instance=request.user.patientprofileinfo)
        else:
            editprofileinfo_form = DoctorProfileInfoForm(request.POST, instance=request.user.doctorprofileinfo)
        if edituser_form.is_valid() and editprofileinfo_form.is_valid():
            edituser_form.save()
            editprofileinfo_form.save()
            return redirect(reverse('index'))
    else:
        edituser_form = EditProfileForm(instance=request.user)
        if not request.user.is_doctor:
            editprofileinfo_form = PatientEditProfileInfo(request.POST, instance=request.user.patientprofileinfo)
        else:
            editprofileinfo_form = DoctorProfileInfoForm(request.POST, instance=request.user.doctorprofileinfo)
        args = {'edituser_form': edituser_form, 'editprofileinfo_form': editprofileinfo_form}
        return render(request, 'registration/edit_profile.html', args)

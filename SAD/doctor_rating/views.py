from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import User, DoctorProfileInfo
from doctor_rating.models import Rating


@login_required
def rate(request):
    if request.method == 'POST':
        star_value = request.POST.get('rating', '')
        doctor_id = request.POST.get('doctor', '')
        doctor = User.objects.get(pk=doctor_id)
        try:
            rate_object = Rating.objects.get(doctor=doctor, patient=request.user)
            rate_object.score = star_value
        except Rating.DoesNotExist:
            rate_object = Rating.objects.create(doctor=doctor, patient=request.user, score=star_value)
        rate_object.save()
        doctor.doctorprofileinfo.score = get_mean_score(doctor)
        doctor.doctorprofileinfo.save()
    return HttpResponseRedirect(reverse('accounts:history'))


def get_mean_score(doctor):
    all_rates = Rating.objects.filter(doctor=doctor).values_list('score', flat=True)
    s = sum(all_rates)
    count = len(all_rates)
    print(count)
    print(all_rates)
    if count == 0:
        score_average = 0.0
    else:
        score_average = s / count
    return score_average

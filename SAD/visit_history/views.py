from django.views.generic import ListView

from accounts.models import User, DoctorProfileInfo
from doctor_calendar.models import Event


# from SAD.doctor_calendar.models import Event

class DoctorListView(ListView):
    template_name = 'visit_history/history.html'
    doctors = None

    def get_queryset(self):
        doctors = Event.objects.filter(patient_user=self.request.user.pk)
        self.doctors = DoctorProfileInfo.objects.none()
        for i in doctors:
            self.doctors |= DoctorProfileInfo.objects.filter(user=i.doctor_user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = self.doctors
        # print("sdsdsdsD ", context['doctors'])
        return context

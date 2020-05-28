from django.views.generic import ListView

from accounts.models import User, PatientProfileInfo
from doctor_calendar.models import Event


class PatientListView(ListView):
    template_name = 'patient_list/list.html'
    patients = None
    patient_info = None

    def get_queryset(self):
        patients = Event.objects.filter(doctor_user=self.request.user.pk)
        self.patients = PatientProfileInfo.objects.none()
        # self.patients_info = PatientProfileInfo.objects.none()
        for i in patients:
            self.patients |= PatientProfileInfo.objects.filter(user=i.patient_user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = self.patients
        return context

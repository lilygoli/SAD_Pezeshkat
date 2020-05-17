from django.views.generic import TemplateView, ListView

from django.db.models import Q
from accounts.models import DoctorProfileInfo
# from SAD.accounts.models import DoctorProfileInfo


class HomePageView(TemplateView):
    template_name = 'search/search_page.html'


class SearchResultsView(ListView):
    model = DoctorProfileInfo
    template_name = 'search/search_results.html'

    def get_queryset(self):
        query_name = self.request.GET.get('q1')
        query_family_name = self.request.GET.get('q2')
        query_speciality = self.request.GET.get('q3')
        object_list = DoctorProfileInfo.objects.filter(
            Q(specialty__contains=query_speciality) & Q(user__name__contains=query_name) & Q(
                user__family_name__contains=query_family_name))
        return object_list

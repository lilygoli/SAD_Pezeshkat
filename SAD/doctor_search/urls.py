from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from doctor_search import views as v

app_name = 'doctor_search'
urlpatterns = [
    url(r'^search_result/', login_required(v.SearchResultsView.as_view()), name='search_results'),
    url(r'^search_page/', login_required(v.HomePageView.as_view()), name='search_page'),
]

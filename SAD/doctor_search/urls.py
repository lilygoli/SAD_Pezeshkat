from django.conf.urls import url
from doctor_search import views as v

app_name = 'doctor_search'
urlpatterns = [
    url(r'^search_result/', v.SearchResultsView.as_view(), name='search_results'),
    url(r'^search_page/', v.HomePageView.as_view(), name='search_page'),
]

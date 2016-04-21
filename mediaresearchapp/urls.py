from django.conf.urls import url, include
from mediaresearchapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Media
    url(r'^startup/(?P<id>[0-9a-zA-Z@.]+)',
        views.StartupViewSet.as_view()),
    url(r'^dashboard/',
        views.ResearchDashboardViewSet.as_view()),
    url(r'^_search/', views.ResearchViewSet.as_view()),
    # structured queries, city=""&..
    url(r'^_sql/', views.SqlResearchViewSet.as_view()),
    # designed to return most recent campaigns.
    url(r'^', views.BasicResearchViewSet.as_view())
]

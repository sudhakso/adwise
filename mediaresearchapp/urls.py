from django.conf.urls import url, include
from mediaresearchapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Media
    url(r'^dashboard/',
        views.ResearchDashboardViewSet.as_view()),
    url(r'^', views.BasicResearchViewSet.as_view())
]

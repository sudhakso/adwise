from django.conf.urls import url, include
from mediaresearchapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^search/', views.CampaignResearchViewSet.as_view()),
    # structured queries, city=""&..
    url(r'^query/', views.QueryViewSet.as_view()),
]

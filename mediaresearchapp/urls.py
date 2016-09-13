from django.conf.urls import url, include
from mediaresearchapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^search/campaign/', views.CampaignResearchViewSet.as_view()),
    url(r'^search/mediaaggregate/',
        views.MediaAggregateResearchViewSet.as_view()),
    url(r'^search/_sql/', views.SqlResearchViewSet.as_view()),
    url(r'^search/', views.ResearchViewSet.as_view()),
]

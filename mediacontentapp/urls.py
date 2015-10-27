from django.conf.urls import url, include
from mediacontentapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Media
    url(r'^ads/$', views.AdViewSet.as_view()),
    url(r'^ads/textads/', views.TextAdViewSet.as_view())
]

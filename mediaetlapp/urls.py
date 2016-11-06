from django.conf.urls import url, include
from mediaetlapp.views import EtlViewSet

# Wire up our API using automatic URL routing.
urlpatterns = [
     url(r'^(?P<source_type>[a-zA-Z]+)/(?P<source_id>[0-9a-zA-Z]+)',
         EtlViewSet.as_view()),
]

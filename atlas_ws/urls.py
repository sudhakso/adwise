from django.conf.urls import url, include
from django.conf.urls import include, url
from userapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    # Media
    url(r'^mediacontent/', include('mediacontentapp.urls')),
    # User
    url(r'^users/', include('userapp.urls')),
    # Documentation engine
    url(r'^', include('rest_framework_swagger.urls')),
    #django-gcm
#     url(r'', include('gcm.urls'))
    # haystack urls
    url(r'^search/', include('haystack.urls')),
]

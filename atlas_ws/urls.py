from django.conf.urls import url, include
from userapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users/', views.UserViewSet.as_view()),
    # TBD
    url(r'^users/(?P<username>[0-9a-zA-Z])/$',\
        views.UserSummaryViewSet),
    # TBD
    url(r'^users/(?P<username>[0-9a-zA-Z])/devices/(?P<devicetype>[a-zA-Z])/$',\
        views.DeviceViewSet),
    # TBD               
    url(r'^users/(?P<username>[0-9a-zA-Z])/devices/(?P<devicetype>[a-zA-Z])/(?P<deviceid>[0-9a-zA-Z])/$',\
        views.DeviceSummaryViewSet),
    # TBD               
    url(r'^users/(?P<username>[0-9a-zA-Z])/preferences/$',\
        views.PreferenceViewSet),
    # TBD               
    url(r'^users/(?P<username>[0-9a-zA-Z])/preferences/(?P<preferencetype>[a-zA-Z])/$',\
        views.PreferenceSummaryViewSet),
    # Documentation engine
    url(r'^', include('rest_framework_swagger.urls')),
    # Media
    url(r'^mediacontent/', include('mediacontentapp.urls')),
]

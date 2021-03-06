from django.conf.urls import url, include

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browse-able API.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    # Media
    url(r'^mediacontent/', include('mediacontentapp.urls')),
    # User
    url(r'^users/', include('userapp.urls')),
    # User
    url(r'^research/', include('mediaresearchapp.urls')),
    # Modeller
    url(r'^modeller/', include('modeller.urls')),
    # Documentation engine
    url(r'^', include('rest_framework_swagger.urls')),
]

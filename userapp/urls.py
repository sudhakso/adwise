from django.conf.urls import url, include
from userapp import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # User
    url(r'^login/$',
        views.login),
    url(r'^services/(?P<userid>[0-9a-zA-Z]+)/$',
        views.UserServiceViewSet.as_view()),
    url(r'^services/(?P<service_key>[0-9a-zA-Z]+)/data/',
        views.UserServiceHandlerViewSet.as_view()),
    url(r'^services/(?P<userid>[0-9a-zA-Z]+)/(?P<service_name>[a-zA-Z]+)/$',
        views.UserServiceViewSet.as_view()),
    url(r'^(?P<userid>[0-9a-zA-Z]+)/$', views.UserViewSet.as_view()),
    url(r'^', views.UserViewSet.as_view())
    ]


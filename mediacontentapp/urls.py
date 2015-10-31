from django.conf.urls import url, include
from mediacontentapp import views, sourceviews

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Media
    url(r'^ads/$', views.AdViewSet.as_view()),
    url(r'^ads/textads/', views.TextAdViewSet.as_view()),
    url(r'^ads/callads/', views.CallOnlyAdViewSet.as_view()),
    url(r'^mediasource/', views.CallOnlyAdViewSet.as_view()),
    url(r'^mediasource/ooh/', sourceviews.OOHMediaSourceViewSet.as_view()),
    url(r'^mediasource/digital/',
        sourceviews.DigitalMediaSourceViewSet.as_view()),
    url(r'^mediasource/vod/', sourceviews.VODMediaSourceViewSet.as_view()),
    url(r'^mediasource/radio/', sourceviews.RadioMediaSourceViewSet.as_view()),
]

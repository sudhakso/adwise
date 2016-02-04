from django.conf.urls import url, include
from mediacontentapp import views, sourceviews

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Media
    url(r'^mediasource/ooh/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.OOHMediaSourceViewSet.as_view()),
    url(r'^mediasource/ooh/',
        sourceviews.OOHMediaSourceViewSet.as_view()),
    url(r'^mediasource/ooh/search/$',
        sourceviews.OOHMediaSourceSearchViewSet.as_view()),
    url(r'^images/(?P<image_id>[0-9a-zA-Z]+)/$',
        views.JpegImageViewSet.as_view())]

'''
#     url(r'^ads/$', views.AdViewSet.as_view()),
#     url(r'^ads/textads/', views.TextAdViewSet.as_view()),
#     url(r'^ads/callads/', views.CallOnlyAdViewSet.as_view()),
#     url(r'^ads/imageads/images/(?P<image_id>[0-9a-zA-Z]+)/$',
#         views.ImageViewSet.as_view()),
#     url(r'^ads/imageads/(?P<campaign_id>[0-9a-zA-Z]+)/$',
#         views.ImageAdViewSet.as_view()),
#     url(r'^ads/imageads/(?P<campaign_id>[0-9a-zA-Z]+)/(?P<ad_id>[0-9a-zA-Z]+)',
#         views.ImageAdViewSet.as_view()),
#     url(r'^campaign/(?P<username>[0-9a-zA-Z]+)/',
#         views.CampaignViewSet.as_view()),
#     url(r'^mediasource/digital/$',
#         sourceviews.DigitalMediaSourceViewSet.as_view()),
#     url(r'^mediasource/vod/$',
#         sourceviews.VODMediaSourceViewSet.as_view()),
#     url(r'^mediasource/radio/$',
#         sourceviews.RadioMediaSourceViewSet.as_view()),
'''

from django.conf.urls import url, include
from mediacontentapp import views, sourceviews, analyticsviews
from mediacontentapp.analyticsviews import AnalyticsViewSet

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Dash-board
    url(r'^dashboard/',
        views.DashboardViewSet.as_view()),
    # Search Query
    url(r'^mediasource/ooh/search/$',
        sourceviews.OOHMediaSourceSearchViewSet.as_view()),
    # Activity Tracker
    url(r'^mediasource/activity/(?P<activity>[a-z]+)/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.MediaSourceActivityTracker.as_view()),
    url(r'^mediasource/tags/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.MediaSourceTagViewSet.as_view()),
    # Media aggregate types
    url(r'^mediaaggregates/types/$',
        sourceviews.MediaAggregateTypeViewSet.as_view()),
    url(r'^mediaaggregates/types/(?P<type_id>[0-9a-zA-Z]+)',
        sourceviews.MediaAggregateTypeViewSet.as_view()),
    # Media aggregates
    url(r'^mediaaggregates/(?P<aggregate_id>[0-9a-zA-Z]+)/addsource/(?P<source_type>[a-zA-Z]+)/(?P<source_id>[0-9a-zA-Z]+)',
        sourceviews.MediaAggregateSourceAddViewSet.as_view()),
    url(r'^mediaaggregates/(?P<aggregate_id>[0-9a-zA-Z]+)/',
        sourceviews.MediaAggregateViewSet.as_view()),
    url(r'^mediaaggregates/',
        sourceviews.MediaAggregateViewSet.as_view()),
    # Media source
    url(r'^mediasource/ooh/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.OOHMediaSourceViewSet.as_view()),
    url(r'^mediasource/ooh/',
        sourceviews.OOHMediaSourceViewSet.as_view()),
    # Campaign
    url(r'^campaign/_index/$',
        views.CampaignIndexingViewSet.as_view()),
    url(r'^campaign/(?P<camp_id>[0-9a-zA-Z]+)/track/$',
        views.CampaignTrackingViewSet.as_view()),
    url(r'^campaign/(?P<camp_id>[0-9a-zA-Z]+)/$',
        views.CampaignViewSet.as_view()),
    url(r'^campaign/',
        views.CampaignViewSet.as_view()),
    # Image repository
    url(r'^images/(?P<image_id>[0-9a-zA-Z]+)/$',
        views.JpegImageViewSet.as_view()),
    # Advertisement repository
    url(r'^ads/$', views.AdViewSet.as_view()),
    url(r'^ads/imageads/images/(?P<image_id>[0-9a-zA-Z]+)/$',
        views.ImageViewSet.as_view()),
    url(r'^ads/imageads/(?P<campaign_id>[0-9a-zA-Z]+)/$',
        views.ImageAdViewSet.as_view()),
    url(r'^ads/imageads/(?P<campaign_id>[0-9a-zA-Z]+)/(?P<ad_id>[0-9a-zA-Z]+)',
        views.ImageAdViewSet.as_view()),
    url(r'^ads/imageads/$',
        views.ImageAdViewSet.as_view()),
    url(r'^ads/textads/', views.TextAdViewSet.as_view()),
    url(r'^ads/callads/', views.CallOnlyAdViewSet.as_view()),
    url(r'^etl/(?P<source_type>[a-zA-Z]+)/(?P<source_id>[0-9a-zA-Z]+)',
        analyticsviews.AnalyticsViewSet.as_view()),
]

#     url(r'^mediasource/digital/$',
#         sourceviews.DigitalMediaSourceViewSet.as_view()),
#     url(r'^mediasource/vod/$',
#         sourceviews.VODMediaSourceViewSet.as_view()),
#     url(r'^mediasource/radio/$',
#         sourceviews.RadioMediaSourceViewSet.as_view())]

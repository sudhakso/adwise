from django.conf.urls import url, include
from mediacontentapp import views, sourceviews

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # Dash-board
    url(r'^dashboard/',
        views.DashboardViewSet.as_view()),
    # Modify playing List
    url(r'^mediasource/playing/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.PlayingViewSet.as_view()),
    # Activity Tracker
    url(r'^mediasource/activity/(?P<activity>[a-z]+)/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.MediaSourceActivityTracker.as_view()),
    url(r'^mediasource/tags/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.MediaSourceTagViewSet.as_view()),
    url(r'^activity/(?P<content_type>[a-z]+)/(?P<activity>[a-z]+)/(?P<id>[0-9a-zA-Z]+)/$',
        sourceviews.MediaContentActivityTracker.as_view()),
    url(r'^activity/(?P<content_type>[a-z]+)/(?P<id>[0-9a-zA-Z]+)/$',
        sourceviews.MediaContentActivityTracker.as_view()),
    # Media aggregate types
    url(r'^mediaaggregates/types/$',
        sourceviews.MediaAggregateTypeViewSet.as_view()),
    url(r'^mediaaggregates/types/(?P<type_id>[0-9a-zA-Z]+)',
        sourceviews.MediaAggregateTypeViewSet.as_view()),
    # Media aggregates
    url(r'^mediaaggregates/(?P<aggregate_id>[0-9a-zA-Z]+)/extensions/$',
        sourceviews.MediaAggregateExtensionViewSet.as_view()),
    url(r'^mediaaggregates/(?P<aggregate_id>[0-9a-zA-Z]+)/extensions/(?P<extension_name>[a-zA-Z]+)/',
        sourceviews.MediaAggregateExtensionViewSet.as_view()),
    url(r'^mediaaggregates/(?P<aggregate_id>[0-9a-zA-Z]+)/$',
        sourceviews.MediaAggregateViewSet.as_view()),
    url(r'^mediaaggregates/',
        sourceviews.MediaAggregateViewSet.as_view()),
    url(r'^extension/amenity/(?P<extension_name>[a-zA-Z]+)/(?P<extension_id>[0-9a-zA-Z]+)/$',
        sourceviews.AmenityExtensionViewSet.as_view()),
    url(r'^extension/amenity/(?P<extension_name>[a-zA-Z]+)/$',
        sourceviews.AmenityExtensionViewSet.as_view()),
    # Media source
    # ooh
    url(r'^mediasource/ooh/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.OOHMediaSourceViewSet.as_view()),
    url(r'^mediasource/ooh/',
        sourceviews.OOHMediaSourceViewSet.as_view()),
    # cloud
    url(r'^mediasource/online/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.OnlineMediaSourceViewSet.as_view()),
    # Nearby
    url(r'^mediasource/nearby/ooh/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.OOHNearByViewSet.as_view()),
    # Playing
    url(r'^playing/mediaagregate/$',
        sourceviews.MediaAggregatePlayingViewSet.as_view()),
    url(r'^playing/oohmediasource/$',
        sourceviews.OOHSourcePlayingViewSet.as_view()),
    url(r'^playing/onlinemediasource/$',
        sourceviews.OnlineSourcePlayingViewSet.as_view()),
    url(r'^playing/venue/$',
        sourceviews.VenuePlayingViewSet.as_view()),
    url(r'^playing/sensor/$',
        sourceviews.SensorPlayingViewSet.as_view()),
    # Campaign
    url(r'^campaign/_index/$',
        views.CampaignIndexingViewSet.as_view()),
    url(r'^campaign/(?P<camp_id>[0-9a-zA-Z]+)/track/$',
        views.CampaignTrackingViewSet.as_view()),
    url(r'^campaign/playing/(?P<id>[0-9a-zA-Z]+)',
        views.CampaignPlayingViewSet.as_view()),
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
    # Venues
    url(r'^mediasource/venue/(?P<id>[0-9a-zA-Z]+)/activity/$',
        sourceviews.VenueActivityViewSet.as_view()),
    url(r'^mediasource/venue/(?P<id>[0-9a-zA-Z]+)',
        sourceviews.VenueViewSet.as_view()),
    url(r'^mediasource/venue/',
        sourceviews.VenueViewSet.as_view()),
    # sensor activity
    url(r'^mediasource/sensor/(?P<id>[0-9a-zA-Z]+)/activity/$',
        sourceviews.SensorActivityViewSet.as_view()),
]

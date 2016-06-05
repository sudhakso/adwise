'''
Created on May 30, 2016

@author: sonu
'''

from rest_framework.views import APIView
from userapp.JSONFormatter import JSONResponse
from mediacontentapp.models import MediaSource, OOHMediaSource,\
    OOHOperationalDailyDataFeed, OOHProcessedAnalytics
from mediacontentapp.sourceserializers import OOHOperationalDailyDataFeedSerializer
from mediacontentapp import IdentityService
from mongoengine.errors import DoesNotExist
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_501_NOT_IMPLEMENTED
from userapp.faults import UserNotAuthorizedException
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from datetime import datetime

# These managers are acting like utilities, and mostly
# contain static methods to server controlling requests.
auth_manager = IdentityService.IdentityManager()


class AnalyticsViewSet(APIView):
    """ View holding analytics for a media source """

    def post(self, request, source_type, source_id):

        """ Sets and Returns current feed statistics tags for
        Media instance identified by Id.
         ---
         response_serializer: OOHOperationalDailyDataFeedSerializer
        """
        try:
            auth_manager.do_auth(request)
            if id is not None:
                if source_type == 'ooh':
                    source = OOHMediaSource.objects.get(id=source_id)
                    serializer = OOHOperationalDailyDataFeedSerializer(
                                                        data=request.data,
                                                        many=True)
                    # Save the data feed record
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(source_ref=source)
                        return JSONResponse(str('success'),
                                            status=HTTP_201_CREATED)
                elif source_type == 'digitalmedia':
                    return JSONResponse(str('not implemented'),
                                        status=HTTP_501_NOT_IMPLEMENTED)
                elif source_type == 'vod':
                    return JSONResponse(str('not implemented'),
                                        status=HTTP_501_NOT_IMPLEMENTED)
                elif source_type == 'radio':
                    return JSONResponse(str('not implemented'),
                                        status=HTTP_501_NOT_IMPLEMENTED)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)



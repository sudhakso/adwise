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


class EtlViewSet(APIView):
    """ View holding analytics for a media source """

    def get(self, request, source_type, source_id):
        """ Sets and Returns current feed statistics tags for
        Media instance identified by Id.
         ---
         response_serializer: OOHOperationalDailyDataFeedSerializer
        """
        try:
            all_data = False
            auth_manager.do_auth(request)
            start_date = request.query_params['startday'] if 'startday' in\
                request.query_params else None
            end_date = request.query_params['endday'] if 'endday' in\
                request.query_params else datetime.now()
            if start_date is None:
                # get all samples
                all_data = True
            # Get the source
            if source_id is not None:
                if source_type == 'ooh':
                    source = OOHMediaSource.objects.get(id=source_id)
                    if all_data:
                        data = OOHOperationalDailyDataFeed.objects.filter(
                                                            source_ref=source)
                    else:
                        # filter only for a date range
                        data = OOHOperationalDailyDataFeed.objects.filter(
                                                source_ref=source,
                                                feed_timestamp__gt=start_date,
                                                feed_timestamp__lt=end_date)
                    serializer = OOHOperationalDailyDataFeedSerializer(
                                                            data,
                                                            many=True)
                    return JSONResponse(serializer.data, status=HTTP_200_OK)
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
            else:
                return JSONResponse(str("source_id is must."),
                                    status=HTTP_400_BAD_REQUEST)
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
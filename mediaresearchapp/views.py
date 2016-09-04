import json
import time
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND,\
    HTTP_200_OK, HTTP_408_REQUEST_TIMEOUT
from mongoengine.errors import DoesNotExist
# (Note:Sonu): Do not remove this import,
# it will mask the import in swagger.
from mediaresearchapp.serializers import SearchQuerySerializer,\
 CampaignResearchResultSerializer, ResearchResultSerializer
from userapp.models import MediaUser
from mediaresearchapp import querycontroller
# (Note:Sonu): Do not remove this import,
# it will mask the import of task in querycontroller
from mediaresearchapp import tasks


qc = querycontroller.querytype_controller()
SEARCH_TASK_TIMEOUT = 3


def _log_user(request):
    _data = {}
    # Get all Http headers
    import re
    regex = re.compile('^HTTP_')
    head = dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))
    username = head['USERNAME'] if 'USERNAME' in head else 'Anonymous'
    email = head['EMAIL'] if 'EMAIL' in head else 'Anonymous'
    _data['username'] = username
    _data['email'] = email

    # Get the  user details, and pass them back
    # to login caller.
    try:
        usr = MediaUser.objects.get(username=username, email=email)
        _data['userid'] = usr.id
    except DoesNotExist as e:
        pass
    return _data


class ResearchViewSet(APIView):

    def post(self, request):
        """ Returns elements to the user based on
            english language search.
         ---
         request_serializer: SearchQuerySerializer
         response_serializer: ResearchResultSerializer
        """
        try:
            user = _log_user(request)
            _id = user['userid'] if 'userid' in user else None
            # return the dash-board for the user
            sql = SearchQuerySerializer(data=request.data)
            if sql.is_valid(raise_exception=True):
                # Push the sql to search pipeline
                obj = sql.save(userid=_id)
                print 'Search query by user {%s} for String {%s}\
                 in QueryFields {%s} with QueryType {%s}.' % (
                                            user['username'],
                                            obj.raw_strings,
                                            obj.query_fields,
                                            obj.query_type)
                # Research result data (RRD)
                if obj.query_object_type is not None:
                    query_object_type = obj.query_object_type
                # Switch the task based on the object to operate.
                task = qc.create_task(query_object_type)
                rrd = task.delay(args=[],
                                 raw_strings=obj.raw_strings,
                                 fields=obj.query_fields,
                                 query_type=obj.query_type,
                                 ignore_failures=True)
                slept = 0
                timeout = False
                while not rrd.ready():
                    time.sleep(.05)
                    slept = slept + 0.05
                    if slept > SEARCH_TASK_TIMEOUT:
                        timeout = True
                        break
                if rrd.state == "SUCCESS":
                    print "slept = %s" % slept
                    outdata = json.loads(str(rrd.result))
                    return JSONResponse(outdata,
                                        status=HTTP_200_OK)
                elif timeout:
                    return JSONResponse("Search timeout.",
                                        status=HTTP_408_REQUEST_TIMEOUT)
                else:
                    return JSONResponse("Something went wrong terrible. Unknown error!.",
                                        status=HTTP_500_INTERNAL_SERVER_ERROR)
            return JSONResponse("Obfuscated query. Cannot handle error %s" % sql.errors,
                                status=HTTP_400_BAD_REQUEST)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class CampaignResearchViewSet(ResearchViewSet):

    def post(self, request):

        """ Returns elements to the user based on
            english language search.
         ---
         request_serializer: SearchQuerySerializer
         response_serializer: CampaignResearchResultSerializer
        """
        return super(CampaignResearchViewSet, self).post(request)


class MediaAggregateResearchViewSet(ResearchViewSet):

    def post(self, request):

        """ Returns elements to the user based on
            english language search.
         ---
         request_serializer: SearchQuerySerializer
         response_serializer: MediaAggregateResearchResultSerializer
        """
        return super(MediaAggregateResearchViewSet, self).post(request)

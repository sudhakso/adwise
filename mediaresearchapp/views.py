import time
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND,\
    HTTP_200_OK, HTTP_408_REQUEST_TIMEOUT
from mongoengine.errors import DoesNotExist
from mediaresearchapp.serializers import SearchQuerySerializer,\
    ResearchResultSerializer
from userapp.models import MediaUser
from mediacontentapp.serializers import CampaignSerializer
from mediaresearchapp.tasks import BasicSearchTask, CampaignQuerySearchTask
from mediaresearchapp import querycontroller


qc = querycontroller.querytype_controller()
SEARCH_TASK_TIMEOUT = 30


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


class CampaignResearchViewSet(APIView):
    """ search Research """

    def post(self, request):

        """ Returns elements to the user based on
            english language search.
         ---
         request_serializer: SearchQuerySerializer
         response_serializer: ResearchResultSerializer
        """
        try:
            query_type = 'Campaign'
            user = _log_user(request)
            _id = user['userid'] if 'userid' in user else None
            # return the dash-board for the user
            sql = SearchQuerySerializer(data=request.data)
            if sql.is_valid():
                # Push the sql to search pipeline
                obj = sql.save(userid=_id)
                print 'Search query for user {%s}. String {%s}, QueryFields {%s}' % (
                                            user['username'],
                                            obj.raw_strings,
                                            obj.query_fields)
                # Multi-field query
                # Research result data (RRD)
                if obj.query_type is not None:
                    query_type = obj.query_type
                task = qc.create_task(query_type)
                rrd = task.delay(args=[],
                                 raw_strings=obj.raw_strings,
                                 fields=obj.query_fields,
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
                    return JSONResponse(rrd.result,
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
            return JSONResponse("Unknown error.",
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class QueryViewSet(APIView):
    """ query """

    def post(self, request):

        try:
            # return the dash-board for the user
            sql = SearchQuerySerializer(data=request.data)
            if sql.is_valid():
                # Push the sql to search pipeline
                obj = sql.save(userid=None)
                print 'Query type {%s} Query {%s}, QueryFields {%s}' % (
                                            obj.query_type,
                                            obj.raw_strings,
                                            obj.query_fields)
                # Research result data (RRD)
                task = qc.create_task(obj.query_type)
                rrd = task.delay(args=[],
                                 raw_strings=obj.raw_strings,
                                 fields=obj.query_fields,
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
                    return JSONResponse(rrd.result,
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
            return JSONResponse("Unknown error.",
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

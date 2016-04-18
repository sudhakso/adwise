import time
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND,\
    HTTP_200_OK, HTTP_408_REQUEST_TIMEOUT
from mongoengine.errors import DoesNotExist
from mediaresearchapp.serializers import SearchQuerySerializer,\
 StartupLeadsSerializer
from userapp.models import MediaUser
from mediacontentapp.serializers import CampaignSerializer
from mediaresearchapp.models import StartupLeads
from mediaresearchapp.tasks import BasicSearchTask


SEARCH_TASK_TIMEOUT = 30


class StartupViewSet(APIView):

    def get(self, request, id=None):

        """ Returns if a startup lead object exists
         ---
         response_serializer: StartupLeadsSerializer
        """
        try:
            if id:
                sl = StartupLeads.objects.get(email=id)
            # Serialize the lead collected.
            serializer = StartupLeadsSerializer(sl)
            return JSONResponse(serializer.data)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id=None):

        """ Creates a startup lead for a user
         ---
         request_serializer: StartupLeadsSerializer
         response_serializer: StartupLeadsSerializer
        """
        try:
            # Serialize the Campaign
            serializer = StartupLeadsSerializer(
                                        data=request.data, partial=True)
            if serializer.is_valid():
                if id:
                    inst = StartupLeads.objects.get(email=id)
                    serializer.update(inst, serializer.validated_data)
                else:
                    serializer.save()
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
            else:
                return JSONResponse(serializer.errors,
                                    status=HTTP_400_BAD_REQUEST)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return JSONResponse(serializer.errors,
                                status=HTTP_400_BAD_REQUEST)


class ResearchDashboardViewSet(APIView):
    pass


class BasicResearchViewSet(APIView):

    """ Basic Research """

    def _log_user(self, request):
        # Get all Http headers
        import re
        regex = re.compile('^HTTP_')
        head = dict((regex.sub('', header), value) for (header, value)
                    in request.META.items() if header.startswith('HTTP_'))
        username = head['USERNAME']
        email = head['EMAIL']
        # Get the  user details, and pass them back
        # to login caller.
        usr = MediaUser.objects.get(username=username, email=email)
        return usr

    def post(self, request):

        """ Returns all research elements to the user
         ---
         request_serializer: SearchQuerySerializer
         response_serializer: ResearchResultSerializer
        """
        try:
            user = self._log_user(request)
            # return the dash-board for the user
            sql = SearchQuerySerializer(data=request.data)
            if sql.is_valid():
                # Push the sql to search pipeline
                obj = sql.save(user=user)
                print 'Search query for user {%s}. String {%s}' % (
                                            user.username, obj.raw_strings)
                # Research result data (RRD)
                task = BasicSearchTask()
                rrd = task.delay(args=[],
                                 raw_strings=obj.raw_strings,
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

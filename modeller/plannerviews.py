from rest_framework.views import APIView
from django.conf import settings
from userapp.JSONFormatter import JSONResponse
from rest_framework.status import HTTP_200_OK,\
    HTTP_408_REQUEST_TIMEOUT, HTTP_500_INTERNAL_SERVER_ERROR
from serializers import OOHPlanRequestSerializer, NotificationRequestSerializer
from celery.canvas import chain
import time
import json
from modeller.tasks import ClassifierTask, FindOOHFiltered, UserSelectorTask,\
 CloudNotifierTask


# Create your views here.
class OOHPlanner(APIView):
    # Classify the input request, and list the billboards
    # meeting the criteria
    def post(self, request):
        try:
            planrequest = OOHPlanRequestSerializer(data=request.data)
            if planrequest.is_valid(raise_exception=True):
                req = planrequest.save()
                # Process the request
                classifier = ClassifierTask()
                findooh = FindOOHFiltered()
                result = chain(classifier.s(req.wish),
                               findooh.s(req.filters)).apply_async()
                slept = 0
                timeout = False
                while not result.ready():
                    time.sleep(.05)
                    slept = slept + 0.05
                    if slept > 3:
                        timeout = True
                        break
                if result.state == "SUCCESS":
                    print "slept = %s" % slept
                    outdata = json.loads(str(result.result))
                    return JSONResponse(outdata,
                                        status=HTTP_200_OK)
                elif timeout:
                    return JSONResponse("Query timeout.",
                                        status=HTTP_408_REQUEST_TIMEOUT)
                else:
                    return JSONResponse("Bad Request!.",
                                        status=HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JSONResponse("Bad Request!.",
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class NotifierView(APIView):
    # Handle notification data
    def post(self, request):
        try:
            notifrequest = NotificationRequestSerializer(data=request.data)
            if notifrequest.is_valid(raise_exception=True):
                req = notifrequest.save()
                print 'Request to send notif type %s with content %s' % (
                                                req.type,
                                                str(req.content).encode('utf-8'))
                # Workaround : GCM apis do not accept u' in begininig of Unicode strings.
                # strip that from the request.
                if req.type == 'data':
                    content = str(req.content).replace("u\"","\"").replace("u\'","\'")
                elif req.type == 'notification':
                    content = req.message
                # Process the request
                users = UserSelectorTask()
                notifier = CloudNotifierTask()
                result = chain(users.s(req.selector),
                               notifier.s(req.topic, req.type, content)).apply_async()
                slept = 0
                timeout = False
                while not result.ready():
                    time.sleep(.05)
                    slept = slept + 0.05
                    if slept > 3:
                        timeout = True
                        break
                if result.state == "SUCCESS":
                    print "slept = %s" % slept
                    outdata = json.loads(str(result.result))
                    return JSONResponse(outdata,
                                        status=HTTP_200_OK)
                elif timeout:
                    return JSONResponse("Query timeout.",
                                        status=HTTP_408_REQUEST_TIMEOUT)
                else:
                    return JSONResponse("Bad Request!.",
                                        status=HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JSONResponse("Bad Request!.",
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

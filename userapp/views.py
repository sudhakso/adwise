# Create your views here.
from models import MediaUser, Service, UserService, ServiceRequest
from rest_framework import viewsets
from userapp.serializers import UserSerializer, UserServiceSerializer,\
    ServiceRequestSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from datetime import datetime
from userapp.session.sessionmanager import SessionManager

session_mgr = SessionManager()


class UserViewSet(APIView):

    """ User resource """

    serializer_class = UserSerializer
    model = MediaUser

    def get(self, request, *args, **kwargs):
        """ Returns a list of users
         ---
         response_serializer: UserSerializer
        """
        # Request Get, all users
        if request.method == 'GET':
            usrs = MediaUser.objects.all()
            serializer = UserSerializer(usrs, many=True)
            return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):
        """ Creates a user
         ---
         request_serializer: UserSerializer
         response_serializer: UserSerializer
        """
        # Request Post, create user
        if request.method == 'POST':
            try:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data, status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors,
                                        status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                print e
                return JSONResponse(serializer.errors,
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserServiceViewSet(APIView):
    """ Service resource """

    serializer_class = UserServiceSerializer
    model = UserService

    def get(self, request, username, service_name=None):
        """ Returns a list of user service
         ---
         response_serializer: UserServiceSerializer
        """
        if username:
            user = MediaUser.objects.get(username=username)
            svcs = UserService.objects.filter(user_ref=user)
            serializer = UserServiceSerializer(svcs, many=True)
            return JSONResponse(serializer.data)

    def post(self, request, username, service_name):
        """ Creates a service request
         ---
         request_serializer: ServiceRequestSerializer
         response_serializer: UserServiceSerializer
        """
        try:
            tm = datetime.now()
            if username and service_name:
                user = MediaUser.objects.get(username=username)
                svc = Service.objects.get(
                            service_friendly_name=service_name)
                if user and svc:
                    serializer = ServiceRequestSerializer(
                                                data=request.data)
                    if serializer.is_valid():
                        serializer.save(request_time=tm,
                                        target_service_id=svc,
                                        requesting_user_id=user,
                                        target_service_name=service_name)
                        # Prepare the service for the User
                        created_svc = session_mgr.prepare_service(
                                                    user_id=user,
                                                    sess_id=None,
                                                    service_name=service_name,
                                                    args=serializer.data)
                        svc_serializer = UserServiceSerializer(created_svc)
                        return JSONResponse(svc_serializer.data,
                                            status=HTTP_201_CREATED)
            else:
                return JSONResponse(serializer.errors,
                                    status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return JSONResponse(serializer.errors,
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserServiceHandlerViewSet(APIView):

    log_each_request = False

    def post(self, request, service_key):
        """ Creates a service request
         ---
         request_serializer: ServiceRequestSerializer
         response_serializer: ServiceRequestSerializer
        """
        # Request Post, create user
        try:
            tm = datetime.now()
            serializer = ServiceRequestSerializer(data=request.data)
            if service_key is None or serializer.is_valid():
                req = ServiceRequest.objects.create(**serializer.data)
                # Request logs can grow huge,
                # each request data is logged anyways.
                if self.log_each_request:
                    req.save()
                # deliver the service, delegate to service manager
                session_mgr.servicemanager.handle_service_request(
                                                        service_key, req)
                return JSONResponse(serializer.data,
                                    status=HTTP_201_CREATED)
            else:
                return JSONResponse(serializer.errors,
                                    status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return JSONResponse(serializer.errors,
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserSummaryViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    pass

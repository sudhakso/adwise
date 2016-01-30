# Create your views here.
from models import MediaUser, Service, UserService, ServiceRequest
from userapp.serializers import UserSerializer, UserServiceSerializer,\
    ServiceRequestSerializer, UserCreateRequestSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from datetime import datetime
from userapp.session.sessionmanager import SessionManager
from userapp.service.identityservice import IdentityManager
from userapp.faults import UserNotAuthorizedException, UserAlreadyExist


session_mgr = SessionManager()
auth_manager = IdentityManager()


# Handler to check user parameters success.
def login(request):
    try:
        # Get all Http headers
        import re
        regex = re.compile('^HTTP_')
        head = dict((regex.sub('', header), value) for (header, value)
                    in request.META.items() if header.startswith('HTTP_'))
        username = head['USERNAME']
        email = head['EMAIL']
        # Try if Auth driver recognizes the user
        auth_manager.do_auth(request)
        # Get the  user details, and pass them back
        # to login caller.
        usr = MediaUser.objects.get(username=username, email=email)
        serializer = UserSerializer(usr, many=False)
        return JSONResponse(serializer.data)
    except UserNotAuthorizedException as e:
        print e
        return JSONResponse(str(e),
                            status=HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print e
        return JSONResponse(str(e),
                            status=HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print e
        return JSONResponse(str(e),
                            status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(APIView):

    """ User resource """

    serializer_class = UserSerializer
    model = MediaUser

    def get(self, request, *args, **kwargs):
        """ Returns a list of users
         ---
         response_serializer: UserSerializer
        """
        try:
            auth_manager.do_auth(request)
            # Request Get, all users
            usrs = MediaUser.objects.all()
            serializer = UserSerializer(usrs, many=True)
            return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """ Creates a user
         ---
         request_serializer: UserCreateRequestSerializer
         response_serializer: UserCreateRequestSerializer
        """
        # Request Post, create user
        try:
            # Pass header for authentication
            auth_manager.do_create(request)
            serializer = UserCreateRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data,
                                    status=HTTP_201_CREATED)
            else:
                # Clear the temporary Auth session created.
                auth_manager.remove_expired_session(request)
                return JSONResponse(serializer.errors,
                                    status=HTTP_400_BAD_REQUEST)
        except UserAlreadyExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            # Remove the created user.
            auth_manager.remove_expired_session(request)
            return JSONResponse(str(e),
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
        try:
            auth_manager.do_auth(request)
            if username:
                user = MediaUser.objects.get(username=username)
                svcs = UserService.objects.filter(user_ref=user)
                serializer = UserServiceSerializer(svcs, many=True)
                return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, username, service_name):
        """ Creates a service request
         ---
         request_serializer: ServiceRequestSerializer
         response_serializer: UserServiceSerializer
        """
        try:
            auth_manager.do_auth(request)
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
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserServiceHandlerViewSet(APIView):

    log_each_request = False

    # (Note:Sonu) This request is always unauthorized for performance
    # reasons.
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
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserSummaryViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    pass

# Create your views here.
from models import MediaUser, Service, UserService, ServiceRequest
from userapp.serializers import UserSerializer, UserServiceSerializer,\
    ServiceRequestSerializer, UserRoleSerializer,\
    UserDevicePrefSerializer, ProjectSerializer,\
    UserMediaPrefSerializer, UserPersonalPrefSerializer,\
    UserLocationPrefSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND,\
    HTTP_300_MULTIPLE_CHOICES, HTTP_200_OK, HTTP_304_NOT_MODIFIED
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from datetime import datetime
from userapp.session.sessionmanager import SessionManager
from userapp.service.identityservice import IdentityManager
from userapp.faults import UserNotAuthorizedException, UserAlreadyExist
from rest_framework.renderers import JSONRenderer
# from oslo_config import cfg
# from oslo_log import log as logging
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned

session_mgr = SessionManager()
auth_manager = IdentityManager()
# LOG = logging.getLogger(__name__)
# CONF = cfg.CONF
# logging.register_options(CONF)
# logging.setup(CONF, 'adwise')


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
        return JSONResponse(serializer.data, status=HTTP_200_OK)
    except UserNotAuthorizedException as e:
        print e
        return JSONResponse(str(e),
                            status=HTTP_401_UNAUTHORIZED)
    except MultipleObjectsReturned as e:
        print e
        return JSONResponse(str(e),
                            status=HTTP_300_MULTIPLE_CHOICES)
    except DoesNotExist as e:
        print e
        return JSONResponse(str(e),
                            status=HTTP_404_NOT_FOUND)
    except Exception as e:
        print e
        return JSONResponse(str(e),
                            status=HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(APIView):

    """ User resource """

    serializer_class = UserSerializer
    model = MediaUser

    def get(self, request, userid=None):
        """ Returns a list of users
         ---
         response_serializer: UserSerializer
        """
        try:
            auth_manager.do_auth(request)
            if userid is None:
                # Request Get, all users
                usrs = MediaUser.objects.all()
                serializer = UserSerializer(usrs, many=True)
                return JSONResponse(serializer.data)
            else:
                usrs = MediaUser.objects.get(id=userid)
                serializer = UserSerializer(usrs)
                return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_300_MULTIPLE_CHOICES)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    # Update a user instance
    def post_update(self, userobj, request):

        project_id = role = device_pref = personal_pref = media_pref = None
        loc_pref = None
        ser = None
        try:
            # Construct the objects
            if "project" in request.data:
                projserializer = ProjectSerializer(
                                        data=request.data["project"],
                                        partial=True)
                if projserializer.is_valid(raise_exception=True):
                    if userobj.project_id:
                        project_id = projserializer.update(
                                                    userobj.project_id,
                                                    projserializer.validated_data)
                    else:
                        project_id = projserializer.save()
                        userobj.project_id = project_id
            if "role" in request.data:
                roleserializer = UserRoleSerializer(
                                        data=request.data["role"], partial=True)
                if roleserializer.is_valid(raise_exception=True):
                    if userobj.role:
                        role = roleserializer.update(
                                                    userobj.role,
                                                    roleserializer.validated_data)
                    else:
                        role = roleserializer.save()
                        userobj.role = role

            if "device_pref" in request.data:
                devserializer = UserDevicePrefSerializer(
                                        data=request.data["device_pref"],
                                        partial=True, many=True)
                if devserializer.is_valid(raise_exception=True):
                    device_pref = devserializer.save()
                    userobj.device_pref = device_pref

            if "personal_pref" in request.data:
                personalserializer = UserPersonalPrefSerializer(
                                                data=request.data["personal_pref"],
                                                partial=True, many=True)
                if personalserializer.is_valid(raise_exception=True):
                    personal_pref = personalserializer.save()
                    userobj.personal_pref = personal_pref

            if "media_pref" in request.data:
                mediaserializer = UserMediaPrefSerializer(
                                                data=request.data["media_pref"],
                                                partial=True, many=True)
                if mediaserializer.is_valid(raise_exception=True):
                    media_pref = mediaserializer.save()
                    userobj.media_pref = media_pref

            if "loc_pref" in request.data:
                locserializer = UserLocationPrefSerializer(
                                                data=request.data["loc_pref"],
                                                partial=True, many=True)
                if locserializer.is_valid(raise_exception=True):
                    loc_pref = locserializer.save()
                    userobj.loc_pref = loc_pref

            if "user" in request.data:
                userserializer = UserSerializer(
                                            data=request.data["user"],
                                            partial=True)
                if userserializer.is_valid(raise_exception=True):
                    user = userserializer.update(
                                            userobj,
                                            userserializer.validated_data)
                    # update django auth
                    auth_manager.do_update(request, user.username,
                                           user.password)
            userobj.save(last_updated=datetime.now(),
                         last_activity=datetime.now())
            ret_data = UserSerializer(userobj)
            # Updated User successfully.
            return JSONResponse(ret_data.data,
                                status=HTTP_200_OK)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_304_NOT_MODIFIED)

    def post(self, request, userid=None):
        """ Creates or updates a user
         ---
         request_serializer: UserSerializer
         response_serializer: UserSerializer
        """
        # Request Post, create user
        try:
            if 'user' not in request.data:
                return JSONResponse("User field must be present.",
                                    status=HTTP_400_BAD_REQUEST)

            # If user exists, updates the user
            if userid:
                auth_manager.do_auth(request)
                usr = MediaUser.objects.get(id=userid)
                return self.post_update(usr, request)

            # Pass header for authentication
            auth_manager.do_create(request)
            project_id = role = device_pref = personal_pref = media_pref = None
            loc_pref = None
            ser = None
            # Construct the objects
            if 'project' in request.data:
                # Create project
                ser = ProjectSerializer(data=request.data['project'])
                if ser.is_valid(raise_exception=True):
                    project_id = ser.save()

            if 'role' in request.data:
                # Create role
                ser = UserRoleSerializer(data=request.data['role'])
                if ser.is_valid(raise_exception=True):
                    role = ser.save()

            if 'device_pref' in request.data:
                # Apply device preference
                ser = UserDevicePrefSerializer(data=request.data['device_pref'],
                                               many=True)
                if ser.is_valid(raise_exception=True):
                    device_pref = ser.save()

            if 'personal_pref' in request.data:
                # Apply personal preference
                ser = UserPersonalPrefSerializer(data=request.data['personal_pref'],
                                                 many=True)
                if ser.is_valid(raise_exception=True):
                    personal_pref = ser.save()

            if 'media_pref' in request.data:
                # Apply media preference
                ser = UserMediaPrefSerializer(data=request.data['media_pref'],
                                              many=True)
                if ser.is_valid(raise_exception=True):
                    media_pref = ser.save()

            if 'loc_pref' in request.data:
                # Apply location preference
                ser = UserLocationPrefSerializer(data=request.data['loc_pref'],
                                                 many=True)
                if ser.is_valid(raise_exception=True):
                    loc_pref = ser.save()

            # Finally, create the User
            ser = UserSerializer(data=request.data['user'])
            if ser.is_valid(raise_exception=True):
                usr = ser.save(date_joined=datetime.now(),
                               last_updated=datetime.now(),
                               last_activity=datetime.now())
                # Update reference fields
                usr.update(project_id=project_id,
                           role=role,
                           device_pref=device_pref,
                           personal_pref=personal_pref,
                           media_pref=media_pref,
                           loc_pref=loc_pref)
                saved_usr = usr.save()
                ser = UserSerializer(saved_usr)
                # Created the User successfully.
                return JSONResponse(ser.data,
                                    status=HTTP_201_CREATED)
        except UserAlreadyExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_400_BAD_REQUEST)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_300_MULTIPLE_CHOICES)
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

    def get(self, request, userid, service_name=None):
        """ Returns a list of user service
         ---
         response_serializer: UserServiceSerializer
        """
        try:
            auth_manager.do_auth(request)
            user = MediaUser.objects.get(id=userid)
            if service_name:
                svc = Service.objects.get(
                                service_friendly_name=service_name)
                svcs = UserService.objects.filter(
                            user_ref=user,
                            service_id=svc)
            else:
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

    def post(self, request, userid, service_name):
        """ Creates a service request
         ---
         request_serializer: ServiceRequestSerializer
         response_serializer: UserServiceSerializer
        """
        try:
            auth_manager.do_auth(request)
            tm = datetime.now()
            if userid and service_name:
                user = MediaUser.objects.get(id=userid)
                svc = Service.objects.get(
                            service_friendly_name=service_name)
                # Continue processing service request
                serializer = ServiceRequestSerializer(
                                            data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(request_time=tm,
                                    service=svc,
                                    user_ref=user)
                    # Prepare the service for the User
                    # Return if already the service exists for the User.
                    created_svc = session_mgr.prepare_user_service(
                                                user=user,
                                                service=svc)
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

    def get(self, request, service_key):
        """ Gets a service instance
         ---
         response_serializer: ServiceRequestSerializer
        """
        # Request Post, create a service data
        # for e.g. an offer, a notification etc.
        try:
            svc = UserService.objects.get(id=service_key)
            # deliver the service, delegate to service manager
            servicedata = session_mgr.servicemanager.handle_service_get_request(
                                            svc,
                                            request.query_params)
            return JSONResponse(servicedata.data,
                                status=HTTP_200_OK)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    # (Note:Sonu) This request is always unauthorized for performance
    # reasons.
    def post(self, request, service_key):
        """ Creates a service request
         ---
         request_serializer: ServiceRequestSerializer
         response_serializer: ServiceRequestSerializer
        """
        # Request Post, create a service data
        # for e.g. an offer, a notification etc.
        try:
            tm = datetime.now()
            serializer = ServiceRequestSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                svc = UserService.objects.get(id=service_key)
                # deliver the service, delegate to service manager
                session_mgr.servicemanager.handle_service_request(
                                            svc,
                                            JSONRenderer().render(
                                                serializer.data['service_meta']
                                            ))
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

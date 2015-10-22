# Create your views here.
from django.contrib.auth.models import User, Group
from django.views.decorators.http import require_http_methods
from models import MediaUser, PreferenceCategory, PreferenceSubCategory,\
UserMediaPref, UserDevicePref, UserPersonalPref
from rest_framework import viewsets
from userapp.serializers import UserSerializer, PreferenceSerializer, DeviceSerializer
from userapp import JSONFormatter
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer


class UserViewSet(APIView):
    """ User resource """    
    def get(self, request, *args, **kwargs):
        # Request Get, all users
        if request.method == 'GET':
            usrs = MediaUser.objects.all()
            print request.data
            serializer = UserSerializer(usrs, many=True)
            return JSONResponse(serializer.data)
    
    def post(self, request, *args, **kwargs):
        # Request Post, create user
        if request.method == 'POST':
            try: 
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data, status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                print e
                return JSONResponse(serializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, *args, **kwargs):
        pass

class UserSummaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
#     queryset = MediaUser.objects.all()
#     serializer_class = UserSerializer
    pass

class PreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows preferences to be viewed or edited.
    """
    queryset = PreferenceSubCategory.objects.all()
    serializer_class = PreferenceSerializer
    
class PreferenceSummaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows preferences to be viewed or edited.
    """
#     queryset = PreferenceSubCategory.objects.all()
#     serializer_class = PreferenceSerializer
    pass

class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows devices to be viewed or edited.
    """
    queryset = UserDevicePref.objects.all()
    serializer_class = DeviceSerializer
    
class DeviceSummaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
#     queryset = MediaUser.objects.all()
#     serializer_class = UserSerializer
    pass

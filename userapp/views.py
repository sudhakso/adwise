# Create your views here.
from django.contrib.auth.models import User, Group
from models import MediaUser, PreferenceCategory, PreferenceSubCategory,\
UserMediaPref, UserDevicePref, UserPersonalPref
from rest_framework import viewsets
from userapp.serializers import UserSerializer, PreferenceSerializer, DeviceSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MediaUser.objects.all()
    serializer_class = UserSerializer


class PreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows preferences to be viewed or edited.
    """
    queryset = PreferenceSubCategory.objects.all()
    serializer_class = PreferenceSerializer
    
class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows devices to be viewed or edited.
    """
    queryset = UserDevicePref.objects.all()
    serializer_class = DeviceSerializer
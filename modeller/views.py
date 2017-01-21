from rest_framework.views import APIView
import socket
from django.conf import settings
from userapp.JSONFormatter import JSONResponse
from django.shortcuts import render
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_501_NOT_IMPLEMENTED
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from modeller import classifierclient

# Connect the socket to the port where the server is listening
server_address = '/tmp/daemon-nbm.sock'


# Create your views here.
class TextClassifier(APIView):
    def post(self, request):

        """ Classify the message into pre-defined categories.
        """
        # Note(Sonu:TBD) Create classifier once.
        message = request.data['message']
        classifier = classifierclient.Classifier()
        classifieds = classifier.classify(message)
        return JSONResponse(classifieds,
                            status=HTTP_200_OK)


class Classifier(APIView):

    def post(self, request, message):

        """ Modify and Control  classifier properties
        """

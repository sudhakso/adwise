from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,\
    HTTP_200_OK, HTTP_204_NO_CONTENT
from datetime import datetime
from django.http.response import HttpResponse
from mongoengine.errors import DoesNotExist
from mediaresearchapp.serializers import ResearchElementSerializer,\
    ResearchResultSerializer, SearchQuerySerializer
from mediacontentapp.models import Campaign
from mediacontentapp.serializers import CampaignSerializer


class ResearchDashboardViewSet(APIView):
    pass


class BasicResearchViewSet(APIView):

    """ Basic Research """

    def get(self, request):

        """ Returns all research elements to the user
         ---
         request_serializer: SearchQuerySerializer
         response_serializer: ResearchResultSerializer
        """
        try:
            # return the dash-board for the user
            cs = Campaign.objects.all()
            serializer = CampaignSerializer(cs, many=True)
            return JSONResponse(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            print e
            return JSONResponse("Unknown error.", status=HTTP_400_BAD_REQUEST)

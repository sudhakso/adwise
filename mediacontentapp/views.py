from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from mediacontentapp.serializers import AdSerializer, TextAdSerializer
from mediacontentapp.models import Ad,TextAd
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK

class AdViewSet(APIView):
    
    """ Ad resource """
    
    serializer_class = AdSerializer
    model = Ad
    
    def get(self, request, *args, **kwargs):
        """ Returns a list of base ads
         ---
         response_serializer: AdSerializer
        """  
        # Request Get, all users
        if request.method == 'GET':
            return JSONResponse("Not Implemented", status=HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):        
        """ Creates a  base Ad
         ---
         request_serializer: AdSerializer         
         response_serializer: AdSerializer
        """  
        # Request Post, create user
        if request.method == 'POST':
            return JSONResponse("Not Implemented", status=HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pass
    
class TextAdViewSet(APIView):
    
    """ TextAd resource """
    
    serializer_class = TextAdSerializer
    model = TextAd
    
    def get(self, request, *args, **kwargs):
        
        """ Returns a list of textual ads
         ---
         response_serializer: TextAdSerializer
        """  
        # Request Get, all users
        if request.method == 'GET':
            ads = TextAd.objects.all()
            serializer = TextAdSerializer(ads, many=True)
            return JSONResponse(serializer.data)
    
    def post(self, request, *args, **kwargs):
        
        """ Creates a text Ad
         ---
         request_serializer: TextAdSerializer         
         response_serializer: TextAdSerializer
        """  
        # Request Post, create user
        if request.method == 'POST':
            try: 
                serializer = TextAdSerializer(data=request.data)
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
    
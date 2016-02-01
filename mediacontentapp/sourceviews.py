from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from mediacontentapp.models import MediaSource, OOHMediaSource
from mediacontentapp.models import DigitalMediaSource, VODMediaSource,\
        RadioMediaSource
from mediacontentapp.sourceserializers import MediaSourceSerializer,\
        OOHMediaSourceSerializer, VODMediaSourceSerializer,\
        DigitalMediaSourceSerializer, RadioMediaSourceSerializer
from mediacontentapp.serializers import JpegImageContentSerializer
from mediacontentapp import IdentityService
from userapp.faults import UserNotAuthorizedException
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from datetime import datetime
from userapp.models import MediaUser


auth_manager = IdentityService.IdentityManager()


class MediaSourceViewSet(APIView):

    """ Media resource """

    serializer_class = MediaSourceSerializer
    model = MediaSource

    def get(self, request, *args, **kwargs):
        """ Returns a list of media source type
         ---
         response_serializer: MediaSourceSerializer
        """
        # Request Get, all users
        if request.method == 'GET':
            return JSONResponse("Not Implemented", status=HTTP_400_BAD_REQUEST)


class OOHMediaSourceViewSet(APIView):

    """ OOH Media source resource """

    serializer_class = OOHMediaSourceSerializer
    model = OOHMediaSource

    def get(self, request, *args, **kwargs):

        """ Returns a list of OOH media sources
         ---
         response_serializer: OOHMediaSourceSerializer
        """
        # Request Get, all users
        if request.method == 'GET':
            fields = request.query_params
            if 'id' in fields:
                sources = OOHMediaSource.objects.get(id=fields['id'])
                multiple = False
            else:
                """
                TBD : django-filters package not working.
                sources = OOHFilter(request.GET,
                                  queryset=OOHMediaSource.objects.all())
                """
                sources = OOHMediaSource.objects.all()
                multiple = True

            serializer = OOHMediaSourceSerializer(sources, many=multiple)
            return JSONResponse(serializer.data)

    def post(self, request):

        """ Creates a OOH media source in adwise
         ---
         request_serializer: OOHMediaSourceSerializer
         response_serializer: OOHMediaSourceSerializer
        """

        # curl -X POST -S -H 'Accept: application/json'\
        # -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"\
        # http://127.0.0.1:8000/mediacontent/mediasource/ooh/
        try:
            auth_user = auth_manager.do_auth(request)
            # TBD (Note:Sonu) : Differentiate the Service user,
            # on-boarding partner and the owner
            operated_by = MediaUser.objects.get(
                                    username=auth_user.username)
            # Store image'
            imageserializer = JpegImageContentSerializer(
                        data=request.data)
            if imageserializer.is_valid():
                img = imageserializer.save()

            serializer = OOHMediaSourceSerializer(
                                data=request.data)
            if serializer.is_valid():
                src = serializer.save(created_time=datetime.now(),
                                      updated_time=datetime.now(),
                                      primary_image_content=img,
                                      image_url=img.get_absolute_url())
                src.update(operated_by=operated_by, owner=operated_by)
                src.save()
                return JSONResponse(serializer.data,
                                    status=HTTP_201_CREATED)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)

        return JSONResponse(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)


class OOHMediaSourceSearchViewSet(APIView):

    def post(self, request, *args, **kwargs):

        """ Returns a list of OOH media source match ids
        """
        # Request POST, with search string
        results = {}
        status_string = "Sorry!! No matches found."
        if request.method == 'POST':
            fields = request.query_params
            if 'q' in fields:
                search_string = fields['q']
                results['display_message'] = "You searched for: " + search_string
                terms = search_string.split()
                entries = []
                found_entries = {}
                for term in terms:
                    st_entries = OOHMediaSource.objects(street_name__icontains=term)
                    if st_entries:
                        for entry in st_entries:
                            found_entries[entry['id']] = entry
                    ct_entries = OOHMediaSource.objects(city__icontains=term)
                    if ct_entries:
                        for entry in ct_entries:
                            found_entries[entry['id']] = entry
                    state_entries = OOHMediaSource.objects(state__icontains=term)
                    if state_entries:
                        for entry in state_entries:
                            found_entries[entry['id']] = entry
                if found_entries:
                    status_string = "Found the following matches"
                    serializer = OOHMediaSourceSerializer(found_entries.values(), many=True)
                    results['matches'] = serializer.data
                else:
                    results['matches'] = None
                results['status_str'] = status_string
                return JSONResponse(results,
                                    status=HTTP_200_OK)
            else:
                status_string = "Invalid Operation. Please try again"
                return JSONResponse(status_string,
                                    status=HTTP_400_BAD_REQUEST)


class DigitalMediaSourceViewSet(APIView):

    """ Digital Media source resource """

    serializer_class = DigitalMediaSourceSerializer
    model = DigitalMediaSource

    def get(self, request, *args, **kwargs):

        """ Returns a list of Digital media sources
         ---
         response_serializer: DigitalMediaSourceSerializer
        """
        # Request Get, all users
        if request.method == 'GET':
            sources = DigitalMediaSource.objects.all()
            serializer = DigitalMediaSourceSerializer(sources, many=True)
            return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):

        """ Creates a Digital media source
         ---
         request_serializer: DigitalMediaSourceSerializer
         response_serializer: DigitalMediaSourceSerializer
        """
        # Request Post, create user
        if request.method == 'POST':
            try:
                serializer = DigitalMediaSourceSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors,
                                        status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                print e
                return JSONResponse(serializer.errors,
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        pass


class RadioMediaSourceViewSet(APIView):

    """ Radio Media source resource """

    serializer_class = RadioMediaSourceSerializer
    model = RadioMediaSource

    def get(self, request, *args, **kwargs):

        """ Returns a list of Digital media sources
         ---
         response_serializer: RadioMediaSourceSerializer
        """
        # Request Get, all users
        if request.method == 'GET':
            sources = RadioMediaSource.objects.all()
            serializer = RadioMediaSourceSerializer(sources, many=True)
            return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):

        """ Creates a Radio media source
         ---
         request_serializer: RadioMediaSourceSerializer
         response_serializer: RadioMediaSourceSerializer
        """
        # Request Post, create user
        if request.method == 'POST':
            try:
                serializer = RadioMediaSourceSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors,
                                        status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                print e
                return JSONResponse(serializer.errors,
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        pass


class VODMediaSourceViewSet(APIView):

    """ VOD Media source resource """

    serializer_class = VODMediaSourceSerializer
    model = VODMediaSource

    def get(self, request, *args, **kwargs):

        """ Returns a list of VOD media sources
         ---
         response_serializer: VODMediaSourceSerializer
        """
        # Request Get, all users
        if request.method == 'GET':
            sources = VODMediaSource.objects.all()
            serializer = VODMediaSourceSerializer(sources, many=True)
            return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):

        """ Creates a VOD media source
         ---
         request_serializer: VODMediaSourceSerializer
         response_serializer: VODMediaSourceSerializer
        """
        # Request Post, create user
        if request.method == 'POST':
            try:
                serializer = VODMediaSourceSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors,
                                        status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                print e
                return JSONResponse(serializer.errors,
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        pass

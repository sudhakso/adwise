from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from mediacontentapp.models import MediaSource, OOHMediaSource
from mediacontentapp.models import DigitalMediaSource, VODMediaSource,\
        RadioMediaSource
from mediacontentapp.sourceserializers import MediaSourceSerializer,\
        OOHMediaSourceSerializer, VODMediaSourceSerializer,\
        DigitalMediaSourceSerializer, RadioMediaSourceSerializer,\
    BookingSerializer, PricingSerializer
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
        sources = None
        multiple = False
        try:
            auth_user = auth_manager.do_auth(request)
            fields = request.query_params
            # OOH-Id
            if 'id' in fields:
                sources = OOHMediaSource.objects.get(id=fields['id'])
                multiple = False
            # User-Id
            # It is very weird MongoDB not supporting join on Reference
            # members.
            elif 'userid' in fields:
                queryUser = MediaUser.objects.get(
                                    username=fields['userid'])
                sources = OOHMediaSource.objects(
                                            owner=queryUser)
                multiple = True if len(sources) > 0 else False
            else:
                sources = OOHMediaSource.objects.all()
                multiple = True

            serializer = OOHMediaSourceSerializer(sources, many=multiple)
            return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)

        return JSONResponse(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)

    def post(self, request, id=None):

        """ Creates a OOH media source in adwise
         ---
         request_serializer: OOHMediaSourceSerializer
         response_serializer: OOHMediaSourceSerializer
        """
        # If it is an update request mentioning id.
        if id:
            return self._update(request, id)

        # curl -X POST -S -H 'Accept: application/json'\
        # -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"\
        # http://127.0.0.1:8000/mediacontent/mediasource/ooh/
        try:
            bookings = None
            img = None
            img_url = None
            pricing = None

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
                img_url = img.get_absolute_url()

            # Store Booking (optional)
            if 'booking' in request.data:
                bookingserializer = BookingSerializer(
                            data=request.data['booking'])
                if bookingserializer.is_valid():
                    bookings = bookingserializer.save()
            # Store Pricing (optional)
            if 'pricing' in request.data:
                pricingserializer = PricingSerializer(
                            data=request.data['pricing'])
                if pricingserializer.is_valid():
                    pricing = pricingserializer.save()
            serializer = OOHMediaSourceSerializer(
                                data=request.data)
            if serializer.is_valid():
                src = serializer.save(created_time=datetime.now(),
                                      updated_time=datetime.now(),
                                      primary_image_content=img,
                                      image_url=img_url)
                src.update(operated_by=operated_by, owner=operated_by,
                           pricing=pricing, booking=bookings)
                src.save()
                return JSONResponse(serializer.data,
                                    status=HTTP_201_CREATED)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)

        return JSONResponse(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)

    def _update(self, request, id):

        """ Updatees given OOH media source
         ---
         request_serializer: OOHMediaSourceSerializer
         response_serializer: OOHMediaSourceSerializer
        """
        try:
            bookings = None
            pricing = None

            auth_user = auth_manager.do_auth(request)
            # TBD (Note:Sonu) : Update the image.
            inst = OOHMediaSource.objects.get(id=id)
            owner = inst.owner
            operated_by = inst.operated_by
            # For any property to be updated, validate
            # that it is done by the user who created it or
            # owns the instance to avoid billboard stealth.
            if owner:
                # Verify if owner is modifying the parameter
                if auth_user.username != owner.username:
                    return JSONResponse(str("Not Authorized"),
                                        status=HTTP_401_UNAUTHORIZED)
            elif operated_by:
                # Verify if the operated by is set to
                # the user requesting the modification.
                if auth_user.username != operated_by.username:
                    return JSONResponse(str("Not Authorized"),
                                        status=HTTP_401_UNAUTHORIZED)
            else:
                # Anonymous user cannot modify Object
                return JSONResponse(str(
                                "Anonymous user cannot modify resources."),
                            status=HTTP_401_UNAUTHORIZED)
            # partial updates
            serializer = OOHMediaSourceSerializer(
                                data=request.data, partial=True)
            if serializer.is_valid():
                updated_obj = serializer.update(inst,
                                                serializer.validated_data)
                # Other reference fields
                # Store image'
                imageserializer = JpegImageContentSerializer(
                            data=request.data)
                if imageserializer.is_valid():
                    img = imageserializer.save()
                    img_url = img.get_absolute_url()
                    updated_obj.update(primary_image_content=img,
                                       image_url=img_url)
                # Store Booking (optional)
                if 'booking' in request.data:
                    bookingserializer = BookingSerializer(
                                data=request.data['booking'])
                    if bookingserializer.is_valid():
                        bookings = bookingserializer.save()
                        updated_obj.update(booking=bookings)
                # Store Pricing (optional)
                if 'pricing' in request.data:
                    pricingserializer = PricingSerializer(
                                data=request.data['pricing'])
                    if pricingserializer.is_valid():
                        pricing = pricingserializer.save()
                        updated_obj.update(pricing=pricing)
                # Verify if Owner change operation is expected.
                fields = request.query_params
                if 'userid' in fields:
                    xfer_ownership_to = MediaUser.objects.get(
                                                    username=fields['userid'])
                    if xfer_ownership_to:
                        updated_obj.update(owner=xfer_ownership_to)
                # Save finally!
                updated_obj.save()
                return JSONResponse(serializer.data,
                                    status=HTTP_200_OK)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)
        # Bad Request
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

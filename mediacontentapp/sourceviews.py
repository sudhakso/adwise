import json
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from mediacontentapp.models import MediaSource, OOHMediaSource
from mediacontentapp.models import DigitalMediaSource, VODMediaSource,\
        RadioMediaSource
from mediacontentapp.models import MediaAggregate, MediaAggregateType
from mediacontentapp.models import MediaDashboard, MediaSourceActivity,\
        SourceTag
from mediacontentapp.sourceserializers import MediaSourceSerializer,\
        OOHMediaSourceSerializer, VODMediaSourceSerializer,\
        DigitalMediaSourceSerializer, RadioMediaSourceSerializer,\
        BookingSerializer, PricingSerializer, MediaSourceActivitySerializer,\
        SourceTagSerializer, MediaAggregateSerializer,\
        MediaAggregateTypeSerializer
from mediacontentapp.serializers import JpegImageContentSerializer
from mediacontentapp import IdentityService
from userapp.faults import UserNotAuthorizedException
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_200_OK,\
    HTTP_404_NOT_FOUND
from datetime import datetime
from userapp.models import MediaUser
from templates import DigitalMediaSourceTemplate

from controller import ActivityManager, TagManager
from typemanager import MediaTypeManager

import logging
from mongoengine.errors import DoesNotExist

# These managers are acting like utilities, and mostly
# contain static methods to server controlling requests.
auth_manager = IdentityService.IdentityManager()
activity_manager = ActivityManager()
tag_manager = TagManager()
category_types = MediaTypeManager()


class MediaAggregateSourceAddViewSet(APIView):
    pass


class MediaAggregateTypeViewSet(APIView):
    """ Media aggregator types """

    def get(self, request, type_id=None):

        """ Returns media aggregator type
        identified by type_id.
        If type_id is None, it returns all
        types defined in the system.
         ---
         response_serializer: MediaAggregateTypeSerializer
        """
        try:
            many = True
            auth_manager.do_auth(request)
            if type_id is not None:
                many = False
                type = MediaAggregateType.objects.get(typename=type_id)
            else:
                type = MediaAggregateType.objects.all()
            # valid activity
            serializer = MediaAggregateTypeSerializer(type, many=many)
            return JSONResponse(serializer.data)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class MediaAggregateViewSet(APIView):
    """ Media source aggregator """

    def __init__(self):
        self.factory = DigitalMediaSourceTemplate()

    def get(self, request, aggregate_id=None):

        """ Returns media aggregator of media instances
        identified by aggregator_id.
         ---
         response_serializer: MediaAggregateSerializer
        """
        try:
            auth_manager.do_auth(request)
            if aggregate_id is not None:
                many = False
                amenity = MediaAggregate.objects.get(id=aggregate_id)
            else:
                many = True
                amenity = MediaAggregate.objects.all()
            serializer = MediaAggregateSerializer(amenity, many=many)
            return JSONResponse(serializer.data)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_update(self, request, amenity):
        """ Registers a Media aggregate
         ---
         request_serializer: MediaAggregateSerializer
         response_serializer: MediaAggregateSerializer
        """
        try:
            img = None
            img_url = None
            icon_img = None
            icon_img_url = None

            # Update existing  aggregator instance
            # Store icon image
            if 'icon_content' in request.data:
                _req = {"image": request.data['icon_content'],
                        "image_type": "png"}
                icon_img_ser = JpegImageContentSerializer(
                            data=_req)
                if icon_img_ser.is_valid(raise_exception=True):
                    icon_img = icon_img_ser.save()
                    icon_img_url = icon_img.get_absolute_url()

            # Store image
            if 'image_content' in request.data:
                _req = {"image": request.data['image_content'],
                        "image_type": "png"}
                img_ser = JpegImageContentSerializer(
                            data=_req)
                if img_ser.is_valid(raise_exception=True):
                    img = img_ser.save()
                    img_url = img.get_absolute_url()

            if 'typespec' in request.data:
                typesepc_ser = MediaAggregateTypeSerializer(
                            data=request.data['typespec'], partial=True)
                if typesepc_ser.is_valid(raise_exception=True):
                    typespec = typesepc_ser.save()

            # Serialize the aggregator object
            serializer = MediaAggregateSerializer(
                                data=request.data, partial=True)
            # Check if serializer is valid
            if serializer.is_valid(raise_exception=True):
                srcobj = serializer.update(amenity, serializer.validated_data)
                srcobj.update(image_content=img,
                              icon_content=icon_img,
                              image_url=img_url,
                              icon_image_url=icon_img_url)
                return JSONResponse(serializer.validated_data,
                                    status=HTTP_200_OK)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, aggregate_id=None):

        """ Registers a Media aggregate
         ---
         request_serializer: MediaAggregateSerializer
         response_serializer: MediaAggregateSerializer
        """
        try:
            img = None
            img_url = None
            icon_img = None
            icon_img_url = None
            typespec = None

            # Authenticate the user
            auth_user = auth_manager.do_auth(request)
            creator = MediaUser.objects.get(username=auth_user.username)

            if aggregate_id is not None:
                # Updates an existing Amenity
                amenity = MediaAggregate.objects.get(id=aggregate_id)
                if amenity.owner == creator:
                    return self.handle_update(request, amenity)
                else:
                    raise UserNotAuthorizedException()
            # Create a new aggregator instance
            # Lookup the type and assign the instance
            typespec = MediaAggregateType.objects.get(
                                        typename=request.data['type'])
            # Store icon image
            if 'icon_content' in request.data:
                icon_img_ser = JpegImageContentSerializer(
                            data=request.data['icon_content'])
                if icon_img_ser.is_valid(raise_exception=True):
                    icon_img = icon_img_ser.save()
                    icon_img_url = icon_img.get_absolute_url()
            # Store image
            if 'image_content' in request.data:
                img_ser = JpegImageContentSerializer(
                            data=request.data['image_content'])
                if img_ser.is_valid(raise_exception=True):
                    img = img_ser.save()
                    img_url = img.get_absolute_url()
            # Serialize the aggregator object
            serializer = MediaAggregateSerializer(
                                data=request.data)
            if serializer.is_valid(raise_exception=True):
                srcobj = serializer.save(created_time=datetime.now(),
                                         image_content=img,
                                         image_url=img_url,
                                         icon_content=icon_img,
                                         icon_image_url=icon_img_url)
                srcobj.update(owner=creator, typespec=typespec)
                # (Note:Sonu)
                # Create a default source and attach it to Aggregate,
                # This default source will host all the in-house campaigns
                # for the aggregate by default.
                # Additional sources can be handled by the aggregate
                # owner
                # Most of the properties are derived from the MediaAggregate
                # property.
                inhouse_source =\
                    self.factory.create_instance(
                        name=srcobj.name,
                        display_name=srcobj.display_name,
                        caption="inhouse source",
                        type=typespec.typename,
                        tags=typespec.category,
                        source_internet_settings=json.dumps(
                                                    srcobj.internet_settings),
                        category=typespec.category,
                        point=srcobj.location)
                srcobj.update(inhouse_source=inhouse_source)
                srcobj.save()
                return JSONResponse(serializer.validated_data,
                                    status=HTTP_201_CREATED)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class MediaSourceTagViewSet(APIView):
    """ Search'able tags """

    def get(self, request, id):

        """ Returns tags for Media instance
        identified by Id.
         ---
         response_serializer: SourceTagSerializer
        """
        try:
            auth_manager.do_auth(request)
            if id is not None:
                # valid activity
                source = OOHMediaSource.objects.get(id=id)
                tags = SourceTag.objects.filter(source_ref=source)
                serializer = SourceTagSerializer(
                                                tags, many=True)
                return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)
        return JSONResponse("", status=HTTP_400_BAD_REQUEST)

    def post(self, request, id):

        """ Logs a named activity for a given media source
         ---
         request_serializer: SourceTagSerializer
         response_serializer: SourceTagSerializer
        """
        try:
            auth_manager.do_auth(request)
            if id is not None:
                source = OOHMediaSource.objects.get(id=id)
                serializer = SourceTagSerializer(data=request.data)
                # Save the activity record
                if serializer.is_valid(raise_exception=True):
                    serializer.save(source_ref=source)
                    return JSONResponse(str('success'),
                                        status=HTTP_201_CREATED)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class MediaSourceActivityTracker(APIView):

    """ Activity tracking """

    def get(self, request, activity, id=None):

        """ Returns named activity counter for
            a Media instance identified by Id.
         ---
         response_serializer: MediaSourceActivitySerializer
        """
        try:
            auth_manager.do_auth(request)
            # TBD (Note:Sonu) Must accept all activities, meaning id=None.
            activity_type = activity_manager.get_activity_id(activity)
            if activity_type != -1 and (
                            id is not None):
                # valid activity
                source = OOHMediaSource.objects.get(id=id)
                activities = MediaSourceActivity.objects.filter(
                                                mediasource=source,
                                                activity_type=activity_type)
                serializer = MediaSourceActivitySerializer(
                                                activities, many=True)
                return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, activity, id=None):

        """ Logs a named activity for a given media source
         ---
         request_serializer: MediaSourceActivitySerializer
         response_serializer: MediaSourceActivitySerializer
        """
        try:
            auth_user = auth_manager.do_auth(request)
            # TBD(Note:Sonu) Id is must.
            activity_type = activity_manager.get_activity_id(activity)
            if activity_type != -1 and (
                            id is not None):
                # valid user
                user = MediaUser.objects.get(username=auth_user.username)
                # valid activity, valid source
                source = OOHMediaSource.objects.get(id=id)
                serializer = MediaSourceActivitySerializer(data=request.data)
                # Save the activity record
                if serializer.is_valid(raise_exception=True):
                    serializer.save(interacting_user=user,
                                    mediasource=source,
                                    activity_type=activity_type,
                                    activity_time=datetime.now())
                    return JSONResponse(str('success'),
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse(str(serializer.errors),
                                        status=HTTP_400_BAD_REQUEST)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


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
            # Workaround: Mongo doesn't support join of ref-field.
            # Billboard owner use case, where only his billboards are
            # shown.
            elif 'userid' in fields:
                queryUser = MediaUser.objects.get(
                                    username=fields['userid'])
                sources = OOHMediaSource.objects(
                                            owner=queryUser)
                multiple = True if len(sources) > 0 else False
            # Media Agency case, where everything should be shown up
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
            return self.handle_update(request, id)

        # curl -X POST -S -H 'Accept: application/json'\
        # -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"\
        # http://127.0.0.1:8000/mediacontent/mediasource/ooh/
        try:
            bookings = None
            img = None
            img_url = None
            pricing = None
            amenities = None

            auth_user = auth_manager.do_auth(request)
            # TBD (Note:Sonu) : Differentiate the Service user,
            # on-boarding partner and the owner
            operated_by = MediaUser.objects.get(
                                    username=auth_user.username)
            # Store image'
            imageserializer = JpegImageContentSerializer(
                        data=request.data)
            if imageserializer.is_valid(raise_exception=False):
                img = imageserializer.save()
                img_url = img.get_absolute_url()

            # Store Booking (optional)
            if 'booking' in request.data:
                bookingserializer = BookingSerializer(
                            data=request.data['booking'])
                if bookingserializer.is_valid(raise_exception=True):
                    bookings = bookingserializer.save()
            # Store Pricing (optional)
            if 'pricing' in request.data:
                pricingserializer = PricingSerializer(
                            data=request.data['pricing'])
                if pricingserializer.is_valid(raise_exception=True):
                    pricing = pricingserializer.save()
            serializer = OOHMediaSourceSerializer(
                                data=request.data)
            if serializer.is_valid(raise_exception=True):
                src = serializer.save(created_time=datetime.now(),
                                      updated_time=datetime.now(),
                                      primary_image_content=img,
                                      image_url=img_url)
                src.update(operated_by=operated_by, owner=operated_by,
                           pricing=pricing, booking=bookings)
                src.save()
                return JSONResponse(serializer.validated_data,
                                    status=HTTP_201_CREATED)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

        return JSONResponse(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)

    def handle_update(self, request, id):

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
            if serializer.is_valid(raise_exception=True):
                updated_obj = serializer.update(inst,
                                                serializer.validated_data)
                # Other reference fields
                # Store image'
                imageserializer = JpegImageContentSerializer(
                            data=request.data)
                if imageserializer.is_valid(raise_exception=False):
                    img = imageserializer.save()
                    img_url = img.get_absolute_url()
                    updated_obj.update(primary_image_content=img,
                                       image_url=img_url)
                # Store Booking (optional)
                if 'booking' in request.data:
                    bookingserializer = BookingSerializer(
                                data=request.data['booking'])
                    if bookingserializer.is_valid(raise_exception=True):
                        bookings = bookingserializer.save()
                        updated_obj.update(booking=bookings)
                # Store Pricing (optional)
                if 'pricing' in request.data:
                    pricingserializer = PricingSerializer(
                                data=request.data['pricing'])
                    if pricingserializer.is_valid(raise_exception=True):
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
            q_str = fields.get('q',None)
            user_obj = auth_manager.do_auth(request)
            entries = []

            if user_obj:
                user_obj = MediaUser.objects.get(username=user_obj.username)
                # Is this guy a Bill board owner?
                if user_obj.role.name == 'BO':
                    entries = OOHMediaSource.objects.filter(owner=user_obj)
                    logging.error("User Entries %s", [e.name for e in entries])
                else:
                # Restrict the search within the city.
                    home_city = user_obj.city
                    if home_city:
                        entries = OOHMediaSource.objects.filter(city=home_city)
                        logging.error("City Entries %s", [e.name for e in entries])
                    else:
                        entries = OOHMediaSource.objects.all()
                        logging.error("All Entries %s", [e.name for e in entries])
                results['display_message'] = "You searched for: " + q_str
                matching_entries = []
                if entries:
                    for e in entries:
#                         logging.error("Entry %s", e.name)
                        if e.name and q_str.upper() in e.name.upper():
                            matching_entries.append(e)
                        elif e.street_name and q_str.upper() in e.street_name.upper():
                            matching_entries.append(e)
                        elif e.city and q_str.upper() in e.city.upper():
                            matching_entries.append(e)

                logging.error("Matching Entries %s", [e.name for e in matching_entries])
                if matching_entries:
                    status_string = "Found the "+str(len(matching_entries)) +" matches"
                    serializer = OOHMediaSourceSerializer(matching_entries, many=True)
                    results['matches'] = serializer.data
                else:
                    results['matches'] = None
                results['status_str'] = status_string
                return JSONResponse(results,
                                    status=HTTP_200_OK)
            else:
                return JSONResponse("UnAuthorized Request",
                                    status=HTTP_401_UNAUTHORIZED)
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
                if serializer.is_valid(raise_exception=True):
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
                if serializer.is_valid(raise_exception=True):
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
                if serializer.is_valid(raise_exception=True):
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

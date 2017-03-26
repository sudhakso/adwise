import json
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from mediacontentapp.models import MediaSource, OOHMediaSource, BrandExtension
from mediacontentapp.models import DigitalMediaSource, VODMediaSource,\
        RadioMediaSource
from mediacontentapp.models import Playing
from mediacontentapp.models import MediaAggregate, MediaAggregateType
from mediacontentapp.models import MediaDashboard, MediaSourceActivity,\
        SourceTag, AmenityExtension, BrandExtension, RetailExtension,\
        FNBExtension, AmenityExtensionCollection
from mediacontentapp.sourceserializers import *
from mediacontentapp.serializers import JpegImageContentSerializer,\
 PlayingSerializer
from mediacontentapp import IdentityService
from userapp.faults import UserNotAuthorizedException
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_200_OK,\
    HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from datetime import datetime
from userapp.models import MediaUser
from templates import DigitalMediaSourceTemplate

from controller import ActivityManager, TagManager, MediaAggregateController,\
  OOHMediaController
from typemanager import MediaTypeManager
from mediacontentapp.etltasks import ExtractNearByAmenitiesTask,\
    AddAmenitiesToBillboardTask
from celery import chain

import logging
from mongoengine.errors import DoesNotExist

# These managers are acting like utilities, and mostly
# contain static methods to server controlling requests.
auth_manager = IdentityService.IdentityManager()
activity_manager = ActivityManager()
tag_manager = TagManager()
category_types = MediaTypeManager()
amentiycontroller = MediaAggregateController()
oohmediacontroller = OOHMediaController()


# Updates the amenity extension instance.
class AmenityExtensionViewSet(APIView):
    # Return serializer instances
    def _deserialize_ex_types(self, extension_name, request, update=False):
        # Creates amenity instances
        ser = None
        if extension_name == 'retail':
            ser = RetailExtensionSerializer(
                                data=request.data,
                                partial=update)
        elif extension_name == 'brand':
            ser = BrandExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'fnb':
            ser = FNBExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'doctor':
            ser = DoctorExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'pharmacy':
            ser = PharmacyExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'facility':
            ser = FacilityExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'emergencyservice':
            ser = EmergencyServiceExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'opdservice':
            ser = opdServiceExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'helpdesk':
            ser = HelpdeskExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'adventuresport':
            ser = AdventureSportExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'specialinterest':
            ser = SpecialInterestExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'staying':
            ser = StayingExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'specialityclinic':
            ser = SpecialityClinicExtensionSerializer(
                                data=request.data,
                                partial=update)
        if extension_name == 'moviemultiplex':
            ser = MultiplexExtensionSerializer(
                                data=request.data,
                                partial=update)
        return ser

    def _serialize_ex_types(self, extension_name, instance):
        # Creates amenity instances
        ser = None
        if extension_name == 'retail':
            ser = RetailExtensionSerializer(instance)
        elif extension_name == 'brand':
            ser = BrandExtensionSerializer(instance)
        if extension_name == 'fnb':
            ser = FNBExtensionSerializer(instance)
        if extension_name == 'doctor':
            ser = DoctorExtensionSerializer(instance)
        if extension_name == 'pharmacy':
            ser = PharmacyExtensionSerializer(instance)
        if extension_name == 'facility':
            ser = FacilityExtensionSerializer(instance)
        if extension_name == 'emergencyservice':
            ser = EmergencyServiceExtensionSerializer(instance)
        if extension_name == 'opdservice':
            ser = opdServiceExtensionSerializer(instance)
        if extension_name == 'helpdesk':
            ser = HelpdeskExtensionSerializer(instance)
        if extension_name == 'adventuresport':
            ser = AdventureSportExtensionSerializer(instance)
        if extension_name == 'specialinterest':
            ser = SpecialInterestExtensionSerializer(instance)
        if extension_name == 'staying':
            ser = StayingExtensionSerializer(instance)
        if extension_name == 'specialityclinic':
            ser = SpecialityClinicExtensionSerializer(instance)
        if extension_name == 'moviemultiplex':
            ser = MultiplexExtensionSerializer(instance)
        return ser

    def handle_update(self, request, extension_name, instance):
        try:
            image = None
            image_url = None
            ser = None
            # Update existing  extension instance
            # Store icon image
            if 'image' in request.data:
                _req = {"image": request.data['image'],
                        "image_type": "png"}
                img_ser = JpegImageContentSerializer(
                            data=_req)
                if img_ser.is_valid(raise_exception=False):
                    image = img_ser.save()
                    image_url = image.get_absolute_url()
            # check the instance type, and load the serializer
            ser = self._deserialize_ex_types(extension_name,
                                           request,
                                           update=True)
            if ser is None:
                return JSONResponse("Unknown instance type %s" % extension_name,
                                    status=HTTP_404_NOT_FOUND)
            # Check if serializer is valid
            if ser.is_valid(raise_exception=True):
                srcobj = ser.update(instance, ser.validated_data)
                srcobj.update(image=image,
                              image_url=image_url)
                return JSONResponse(ser.validated_data,
                                    status=HTTP_200_OK)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, extension_name, extension_id=None):

        """ updates an extension instance.
         ---
         response_serializer: AmenityExtensionSerializer
        """
        # Get the AmenityExtension object instance by Id
        # Determine the type, and load the correct the serializer.
        # Update the content and save.

        # Authenticate the user
        auth_user = auth_manager.do_auth(request)
        creator = MediaUser.objects.get(username=auth_user.username)
        if extension_id is not None:
            amex = AmenityExtension.objects.filter(ex_type=extension_name,
                                                   id=extension_id)
            if amex:
                # Handle update
                return self.handle_update(request, extension_name, amex[0])
            return JSONResponse("Extension id %s for name %s not found" % (
                                                            extension_id,
                                                            extension_name),
                                status=HTTP_404_NOT_FOUND)
        else:
            try:
                ser = self._deserialize_ex_types(extension_name, request)
                # Save the object
                if ser.is_valid(raise_exception=True):
                    _ex = ser.save()
                    _ex.update(userref=creator)
                    return JSONResponse(ser.data,
                                        status=HTTP_201_CREATED)
            except UserNotAuthorizedException as e:
                print e
                return JSONResponse(str(e),
                                    status=HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print e
                return JSONResponse(str(e),
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, extension_name, extension_id=None):
        """ Returns extension by id
         ---
         response_serializer: AmenityExtensionSerializer
        """
        # Authenticate the user
        auth_user = auth_manager.do_auth(request)
        usr = MediaUser.objects.get(username=auth_user.username)
        if extension_id is not None:
            try:
                amex = AmenityExtension.objects.filter(id=extension_id)
                # Collect extension data
                if amex:
                    exser = self._serialize_ex_types(extension_name, amex[0])
                    return JSONResponse(exser.data,
                                        status=HTTP_200_OK)
                else:
                    return JSONResponse("Extension with id %s doesn't exists",
                                        status=HTTP_404_NOT_FOUND)
            except Exception as e:
                print e
                return JSONResponse(str(e),
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return all extensions for that user.
            allex = AmenityExtension.objects.filter(userref=usr)
            allexser = AmenityExtensionSerializer(allex, many=True)
            return JSONResponse(allexser.data,
                                status=HTTP_200_OK)


# Creates the extension and adds it to MediaAggregate instance
class MediaAggregateExtensionViewSet(APIView):

    def _serialize_ex_types(self, extension_name, instances):
        # Creates amenity instances
        ser = None
        if extension_name == 'retail':
            ser = RetailExtensionSerializer(instances, many=True)
        elif extension_name == 'brand':
            ser = BrandExtensionSerializer(instances, many=True)
        if extension_name == 'fnb':
            ser = FNBExtensionSerializer(instances, many=True)
        if extension_name == 'doctor':
            ser = DoctorExtensionSerializer(instances, many=True)
        if extension_name == 'pharmacy':
            ser = PharmacyExtensionSerializer(instances, many=True)
        if extension_name == 'facility':
            ser = FacilityExtensionSerializer(instances, many=True)
        if extension_name == 'emergencyservice':
            ser = EmergencyServiceExtensionSerializer(instances, many=True)
        if extension_name == 'opdservice':
            ser = opdServiceExtensionSerializer(instances, many=True)
        if extension_name == 'helpdesk':
            ser = HelpdeskExtensionSerializer(instances, many=True)
        if extension_name == 'adventuresport':
            ser = AdventureSportExtensionSerializer(instances, many=True)
        if extension_name == 'specialinterest':
            ser = SpecialInterestExtensionSerializer(instances, many=True)
        if extension_name == 'staying':
            ser = StayingExtensionSerializer(instances, many=True)
        if extension_name == 'specialityclinic':
            ser = SpecialityClinicExtensionSerializer(instances, many=True)
        if extension_name == 'moviemultiplex':
            ser = MultiplexExtensionSerializer(instances, many=True)
        return ser

    def get(self, request, aggregate_id, extension_name=None):

        """ Returns collection of amenity for an aggregate
         ---
         response_serializer: AmenityExtensionSerializer
        """
        if aggregate_id is not None:
            try:
                ma = MediaAggregate.objects.get(id=aggregate_id)
                # Collect all extensions
                if extension_name:
                    ams = AmenityExtension.objects.filter(amenityref=ma,
                                                          ex_type=extension_name)
                    amser = self._serialize_ex_types(extension_name,
                                                     ams)
                else:
                    ams = AmenityExtension.objects.filter(amenityref=ma)
                    amser = AmenityExtensionSerializer(ams, many=True)
                return JSONResponse(amser.data,
                                    status=HTTP_200_OK)
            except DoesNotExist as e:
                print e
                return JSONResponse(str(e),
                                    status=HTTP_404_NOT_FOUND)
            except Exception as e:
                print e
                return JSONResponse(str(e),
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JSONResponse("aggregate id cannot be none",
                                status=HTTP_400_BAD_REQUEST)

    def post(self, request, aggregate_id):

        """ Adds an existing extension to the Mediaaggregate object.
         ---
         response_serializer: AmenityExtensionSerializer
        """
        # Return an instance of AmenityExtensionCollection
        if aggregate_id is not None:
            try:
                # Authenticate the user
                auth_manager.do_auth(request)
                ma = MediaAggregate.objects.get(id=aggregate_id)
                exids = request.query_params.getlist('ids')
                # Add each extension to the MediaAggregate
                for exid in exids:
                    ex = AmenityExtension.objects.get(id=exid)
                    ex.update(amenityref=ma)
                # Collect all extensions for the MA
                ams = AmenityExtension.objects.filter(amenityref=ma)
                amsser = AmenityExtensionSerializer(ams, many=True)
                return JSONResponse(amsser.data,
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
        else:
            return JSONResponse(str(e),
                                status=HTTP_400_BAD_REQUEST)


class MediaAggregatePlayingViewSet(APIView):

    def get(self, request):

        """ Returns playing relation
         ---
         response_serializer: PlayingSerializer
        """
        try:
            many = True
            auth_manager.do_auth(request)
            params = request.query_params
            if 'id' in params:
                maobj = MediaAggregate.objects.get(id=params['id'])
                if 'all' in params:
                    # Do not filter
                    plays = Playing.objects.filter(
                                    primary_media_source=maobj.inhouse_source)
                else:
                    plays = Playing.objects.filter(
                                    primary_media_source=maobj.inhouse_source,
                                    end_date__gte=datetime.now)
                serializer = PlayingSerializer(plays, many=True)
                return JSONResponse(serializer.data, status=HTTP_200_OK)
            else:
                return JSONResponse('Id cannot be none', status=HTTP_400_BAD_REQUEST)
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


class OOHSourcePlayingViewSet(APIView):

    def get(self, request):

        """ Returns playing relation
         ---
         response_serializer: PlayingSerializer
        """
        try:
            many = True
            auth_manager.do_auth(request)
            params = request.query_params
            if 'id' in params:
                ooh = OOHMediaSource.objects.get(id=params['id'])
                plays = Playing.objects.filter(
                                primary_media_source=ooh,
                                end_date__gte=datetime.now)
                serializer = PlayingSerializer(plays, many=True)
                return JSONResponse(serializer.data, status=HTTP_200_OK)
            else:
                return JSONResponse('Id cannot be none',
                                    status=HTTP_400_BAD_REQUEST)
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
            auth_user = auth_manager.do_auth(request)
            if aggregate_id is not None:
                many = False
                amenity = MediaAggregate.objects.get(id=aggregate_id)
            else:
                many = True
                apply_filters = False
                # Check if type-name is specified.
                filter_by_type = True if 'typename' in request.query_params\
                                        else False
                filter_by_user = True if 'myowned' in request.query_params\
                                        else False
                apply_filters = filter_by_type or filter_by_user
                if apply_filters:
                    if filter_by_type:
                        name = request.query_params['typename']
                        typeobj = MediaAggregateType.objects.get(typename=name)
                    if filter_by_user and request.query_params['myowned']:
                        owner = MediaUser.objects.get(
                                            username=auth_user.username)
                    if filter_by_type and filter_by_user:
                        amenity = MediaAggregate.objects.filter(
                                                        typespec=typeobj,
                                                        owner=owner)
                    elif filter_by_type:
                        amenity = MediaAggregate.objects.filter(
                                                        typespec=typeobj)
                    else:
                        amenity = MediaAggregate.objects.filter(
                                                        owner=owner)
                else:
                    amenity = MediaAggregate.objects.all()
            # Serialize
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
                    do_action = True if 'action' in request.query_params\
                     else False
                    if do_action:
                        action = request.query_params['action']
                        return amentiycontroller.handle_operations(
                                                        amenity,
                                                        action,
                                                        request.query_params,
                                                        request.data)
                    # do the normal update
                    # (Note:Sonu) Add the handle_update operation into
                    # controller.
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
                return JSONResponse(serializer.data,
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
                    activity = serializer.save(activity_type=activity_type,
                                               activity_time=datetime.now())
                    activity.update(interacting_user=user,
                                    mediasource=source)
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


class MediaContentActivityTracker(APIView):

    """ Activity tracking """
    def get(self, request, content_type, id, detail=False):

        """ Gets all activities for a given media content
         ---
         request_serializer: MediaContentActivitySerializer
         response_serializer: MediaContentActivitySerializer
        """
        try:
            acts = []
            auth_user = auth_manager.do_auth(request)
            # valid user
            if content_type == 'campaign':
                content = Campaign.objects.get(id=id)
                acts = MediaContentActivity.objects.filter(
                                                        campaign=content)
            elif content_type == 'ad':
                content = Ad.objects.get(id=id)
                acts = MediaContentActivity.objects.filter(
                                                        ad=content)
            elif content_type == 'offer':
                content = OfferExtension.objects.get(id=id)
                acts = MediaContentActivity.objects.filter(
                                                        offer=content)
            else:
                return JSONResponse(
                        str("Unsupported content type %s" % content_type),
                        status=HTTP_400_BAD_REQUEST)
            # serialize content
            act_ser = MediaContentActivitySerializer(acts,
                                                     many=True)
            return JSONResponse(act_ser.data,
                                status=HTTP_200_OK)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, content_type, activity, id=None):

        """ Logs a named activity for a given media content
         ---
         request_serializer: MediaContentActivitySerializer
         response_serializer: MediaContentActivitySerializer
        """
        try:
            camp_content = None
            ad_content = None
            offer_content = None
            auth_user = auth_manager.do_auth(request)
            # TBD(Note:Sonu) Id is must.
            activity_type = activity_manager.get_activity_id(activity)
            if activity_type != -1 and (
                            id is not None):
                # valid user
                user = MediaUser.objects.get(username=auth_user.username)
                # valid activity, valid source
                if content_type == 'campaign':
                    camp_content = Campaign.objects.get(id=id)
                elif content_type == 'ad':
                    ad_content = Ad.objects.get(id=id)
                elif content_type == 'offer':
                    offer_content = OfferExtension.objects.get(id=id)
                else:
                    return JSONResponse(
                            str("Unsupported content type %s" % content_type),
                            status=HTTP_400_BAD_REQUEST)
                # serialize content
                serializer = MediaContentActivitySerializer(data=request.data)
                # Save the activity record
                if serializer.is_valid(raise_exception=True):
                    activity = serializer.save(activity_type=activity_type,
                                               activity_time=datetime.now())
                    # Activity update
                    activity.update(interacting_user=user,
                                    campaign=camp_content,
                                    ad=ad_content,
                                    offer=offer_content)
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


class OOHNearByViewSet(APIView):
    """ OOH NearBy resource """

    serializer_class = AmenitySerializer
    model = Amenity

    def _discover_amenity_mediasource(self, ooh_instance):
        ooh = OOHMediaSourceIndexSerializer(ooh_instance, many=False)
        data = {'lat': ooh.data['point'][0], 'lon': ooh.data['point'][1]}
        query = """<osm-script>
                    <query type="node">
                        <around lat="{lat}" lon="{lon}" radius="200"/>
                            <has-kv k="amenity" regv="restaurant|bank|school" />
                    </query>
                    <print />
                   </osm-script>"""
        query = query.format(**data)
        # Create a chain of task to discover and add amenities
        task_pipe_1 = ExtractNearByAmenitiesTask()
        task_pipe_2 = AddAmenitiesToBillboardTask()
        res = chain(task_pipe_1.s(querystr=query),
                    task_pipe_2.s(str(ooh_instance.id)))()
        # TBD: state tracking
        res.get()

    def get(self, request, id):
        """ Returns a list of nearby amenities for media source
         ---
         response_serializer: AmenitySerialzer
        """
        # Request Get, all users
        ooh = OOHMediaSource.objects.get(id=id)
        nearbys_qs = NearBy.objects.filter(media_source=ooh)
        if nearbys_qs:
            nearbys = [nearby.amenity for nearby in nearbys_qs]
            ser = AmenitySerializer(nearbys, many=True)
            return JSONResponse(ser.data, status=HTTP_200_OK)
        else:
            return JSONResponse("No amenities found",
                                status=HTTP_204_NO_CONTENT)

    def post(self, request, id):
        """ Returns a list of nearby amenities for media source
         ---
         response_serializer: AmenitySerialzer
        """
        # Request Post
        ooh = OOHMediaSource.objects.get(id=id)
        self._discover_amenity_mediasource(ooh)
        # discover is a synchronous call.
        # Return the list of amenities.
        nearbys_qs = NearBy.objects.filter(media_source=ooh)
        if nearbys_qs:
            nearbys = [nearby.amenity for nearby in nearbys_qs]
            ser = AmenitySerializer(nearbys, many=True)
            return JSONResponse(ser.data, status=HTTP_200_OK)
        else:
            return JSONResponse("Error. No amenities were added.",
                                status=HTTP_204_NO_CONTENT)


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
                return JSONResponse(serializer.data,
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

        """ Updates given OOH media source
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
            # Check if actions?
            do_action = True if 'action' in request.query_params\
                else False
            if do_action:
                action = request.query_params['action']
                return oohmediacontroller.handle_operations(
                                                    inst,
                                                    action,
                                                    request.query_params,
                                                    request.data)
            else:
                # handle partial updates
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
        # Bad Request
        return JSONResponse(serializer.errors,
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

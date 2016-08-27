import json
from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from mediacontentapp.serializers import AdSerializer, TextAdSerializer,\
    CallOnlyAdSerializer, ImageAdSerializer, CampaignSerializer,\
    ImageContentSerializer, JpegImageContentSerializer, CampaignSpecSerializer,\
    CampaignTrackingSerializer, AdExtensionSerializer, OfferExtensionSerializer,\
    CampaignIndexSerializer, SocialMediaExtensionSerializer, T_C_ExtensionSerializer
from mediacontentapp.sourceserializers import MediaDashboardSerializer
from userapp.models import MediaUser
from mediacontentapp.models import Ad, TextAd, CallOnlyAd, ImageAd, Campaign,\
    ImageContent, JpegImageContent, MediaDashboard, CampaignTracking,\
    OfferExtension
from mediacontentapp.tasks import CampaignIndexingTask
from mediacontentapp.controller import CampaignManager
from mediacontentapp.IdentityService import IdentityManager
from mediacontentapp.controller import DashboardController
from mediacontentapp.faults import UserNotAuthorizedException
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,\
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED
from datetime import datetime
from django.http.response import HttpResponse
from mongoengine.errors import DoesNotExist

auth_manager = IdentityManager()
dashboard_controller = DashboardController()


class DashboardViewSet(APIView):

    """ Media Dash-board """

    serializer_class = MediaDashboardSerializer
    model = MediaDashboard

    # Must have dash-board controller.
    # One for 'BO' another for 'MA' for e.g.
    def get(self, request):

        """ Returns dash-board for the user
         ---
         response_serializer: MediaDashboardSerializer
        """
        try:
            auth_user = auth_manager.do_auth(request)
            user = MediaUser.objects.get(
                                    username=auth_user.username)
            # return the dash-board for the user.
            dash = MediaDashboard.objects.get(user=user)
            serializer = MediaDashboardSerializer(dash)
            return JSONResponse(serializer.data, status=HTTP_200_OK)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    # Request to create, if not exist
    # else, refresh
    def post(self, request):

        """ Creates a user dash-board
         ---
         response_serializer: MediaDashboardSerializer
        """
        try:
            auth_user = auth_manager.do_auth(request)
            # ensure user
            user = MediaUser.objects.get(
                                    username=auth_user.username)
            dash = MediaDashboard.objects.filter(user=user)
            if not len(dash):
                # Get the dash-board type
                dash_typ = dashboard_controller.type(
                                    user.role.name if user.role else None)
                # Create for the user
                serializer = MediaDashboardSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    # Create one.
                    inst = serializer.save(user=user,
                                           dashboard_type=dash_typ)
                    updated_inst = serializer.update(inst)
                    serializer = MediaDashboardSerializer(updated_inst)
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
            else:
                # Update the dash-board
                serializer = MediaDashboardSerializer()
                updated_inst = serializer.update(dash[0])
                serializer = MediaDashboardSerializer(updated_inst)
                return JSONResponse(serializer.data, status=HTTP_200_OK)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


class CampaignIndexingViewSet(APIView):

    def post(self, request):

        """ re-creates the indexes for the campaign
        """
        try:
            campset = Campaign.objects.filter(enabled=True)
            if campset:
                cs = CampaignIndexSerializer(campset, many=True)
                task = CampaignIndexingTask()
                rc = task.delay(args=[],
                                instancename=str("__all"),
                                campaign=json.dumps(cs.data),
                                ignore_failures=True,
                                many=True)
                if rc.state == "SUCCESS":
                    return JSONResponse("indexed",
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse("Failed",
                                        status=HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return JSONResponse("no content to index",
                                    status=HTTP_204_NO_CONTENT)
        except Exception as e:
                    return JSONResponse(str(e),
                                        status=HTTP_500_INTERNAL_SERVER_ERROR)


class CampaignViewSet(APIView):

    """ campaign resource """

    serializer_class = CampaignSerializer
    model = Campaign
    # View controller
    controller = CampaignManager()

    def get(self, request, camp_id=None):

        """ Returns a list of campaigns for a user
         ---
         response_serializer: CampaignSerializer
        """
        try:
            cs = None
            auth_user = auth_manager.do_auth(request)
            # valid user
            user = MediaUser.objects.get(username=auth_user.username)
            if camp_id:
                cs = Campaign.objects.filter(creator=user, id=camp_id)
            else:
                cs = Campaign.objects.filter(creator=user)
            if not len(cs):
                return JSONResponse(str("User doesn't have any campaign."),
                                    status=HTTP_204_NO_CONTENT)
            serializer = CampaignSerializer(cs, many=True)
            return JSONResponse(serializer.data)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)

    def post(self, request, camp_id=None):

        """ Creates a campaign for a user
         ---
         request_serializer: CampaignSerializer
         response_serializer: CampaignSerializer
        """
        try:
            spec = None
            create_time = datetime.now()
            auth_user = auth_manager.do_auth(request)
            user = MediaUser.objects.get(username=auth_user.username)

            # Handle update here
            if camp_id:
                return self._update(request, camp_id, user)

            # Serialize spec
            if 'spec' in request.data:
                cspecserializer = CampaignSpecSerializer(
                                            data=request.data['spec'])
                if cspecserializer.is_valid(raise_exception=True):
                    spec = cspecserializer.save()

            img = None
            # Store home page for the campaign
            if 'image' in request.data:
                imageserializer = ImageContentSerializer(
                        data=request.data)
                if imageserializer.is_valid(raise_exception=True):
                    img = imageserializer.save()

            # Serialize the Campaign
            serializer = CampaignSerializer(
                                        data=request.data)
            if serializer.is_valid(raise_exception=True):
                campaign = serializer.save(creation_time=create_time,
                                           creator=user)
                # Campaign created.
                if spec:
                    campaign.update(spec=spec)
                if img:
                    campaign.update(image_content=img,
                                    image_url=img.get_absolute_url())
                # Prepare the campaign for the User
                self.controller.prepare_campaign(
                                            user=user,
                                            camp=campaign,
                                            spec=spec)
                # Create tracker object
                tracker = CampaignTrackingSerializer(data=request.data)
                if tracker.is_valid(raise_exception=True):
                    tracker.save(campaign=campaign)
                return JSONResponse(serializer.data,
                                    status=HTTP_201_CREATED)
            else:
                return JSONResponse(serializer.errors,
                                    status=HTTP_400_BAD_REQUEST)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            return JSONResponse(serializer.errors,
                                status=HTTP_400_BAD_REQUEST)

    def _update(self, request, camp_id, user):
        """ Updates given campaign instance
         ---
         request_serializer: CampaignSerializer
         response_serializer: CampaignSerializer
        """
        try:
            spec = None
            # TBD (Note:Sonu) : Update the image.
            inst = Campaign.objects.get(id=camp_id, creator=user)
            # For any property to be updated, validate
            # that it is done by the user who created it or
            # owns the instance to avoid billboard stealth.
            if not inst:
                # Verify if owner is modifying the parameter
                return JSONResponse(str("Not Authorized"),
                                    status=HTTP_401_UNAUTHORIZED)
            # partial updates
            serializer = CampaignSerializer(
                                data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                updated_obj = serializer.update(inst,
                                                serializer.validated_data)
                # Other reference fields
                # Store image'
                if "spec" in request.data:
                    specserializer = CampaignSpecSerializer(
                                            data=request.data["spec"], partial=True)
                    if specserializer.is_valid(raise_exception=True):
                        spec = specserializer.update(updated_obj.spec,
                                                     specserializer.validated_data)
                if "image" in request.data:
                    imageserializer = ImageContentSerializer(
                                        data=request.data, partial=True)
                    # Bug (Sonu:) how to change the image URL? or the
                    # image URL is retained. Need to be checked.
                    # Post image update, image show may not work correctly.
                    if imageserializer.is_valid(raise_exception=True):
                        img = imageserializer.save()
                        updated_obj.update(image_content=img,
                                           image_url=img.get_absolute_url())
                        updated_obj.save()
                return JSONResponse(serializer.validated_data,
                                    status=HTTP_200_OK)
        except Exception as e:
            print e
        return JSONResponse(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)


class CampaignTrackingViewSet(APIView):
    """ campaign tracking resource """

    serializer_class = CampaignTrackingSerializer
    model = CampaignTracking
    # View controller
    controller = CampaignManager()

    def get(self, request, camp_id):

        """ Returns a tracking object for the campaigns
         ---
         response_serializer: CampaignTrackingSerializer
        """
        try:
            auth_user = auth_manager.do_auth(request)
            # valid user
            user = MediaUser.objects.get(username=auth_user.username)
            camp = Campaign.objects.get(creator=user, id=camp_id)
            track = CampaignTracking.objects.get(campaign=camp)
            serializer = CampaignTrackingSerializer(track)
            return JSONResponse(serializer.data)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)


class AdViewSet(APIView):

    """ Ad resource """

    serializer_class = AdSerializer
    model = Ad

    # meta
    meta = {'allow_inheritance': True}

    # TBD(sonu:) Get all ads defined.
    # Serialize only Ad structure
    def get(self, request, *args, **kwargs):
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
        try:
            auth_manager.do_auth(request.META)
            # Request Get, all users
            if request.method == 'GET':
                ads = TextAd.objects.all()
                serializer = TextAdSerializer(ads, many=True)
                return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):

        """ Creates a text Ad
         ---
         request_serializer: TextAdSerializer
         response_serializer: TextAdSerializer
        """
        # Request Post, create user
        if request.method == 'POST':
            try:
                auth_manager.do_auth(request.META)
                serializer = TextAdSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors,
                                        status=HTTP_400_BAD_REQUEST)
            except UserNotAuthorizedException as e:
                print e
                return JSONResponse(str(e), status=HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print e
                return JSONResponse(serializer.errors,
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)


class CallOnlyAdViewSet(AdViewSet):

    """ Call Only Campaign resource """

    serializer_class = CallOnlyAdSerializer
    model = CallOnlyAd

    def get(self, request, *args, **kwargs):

        """ Returns a list of call only campaign ads
         ---
         response_serializer: CallOnlyAdSerializer
        """
        try:
            auth_manager.do_auth(request.META)
            # Request Get, all users
            if request.method == 'GET':
                ads = CallOnlyAd.objects.all()
                serializer = CallOnlyAdSerializer(ads, many=True)
                return JSONResponse(serializer.data)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e), status=HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):

        """ Creates a Call only campaign Ad
         ---
         request_serializer: CallOnlyAdSerializer
         response_serializer: CallOnlyAdSerializer
        """
        # Request Post, create user
        if request.method == 'POST':
            try:
                auth_manager.do_auth(request.META)
                serializer = CallOnlyAdSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors,
                                        status=HTTP_400_BAD_REQUEST)
            except UserNotAuthorizedException as e:
                print e
                return JSONResponse(str(e), status=HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print e
                return JSONResponse(serializer.errors,
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)


class ImageViewSet(AdViewSet):
    """ Returns Image resource """

    serializer_class = ImageAdSerializer
    model = ImageContent

    # curl -X GET -S -H 'Accept: application/json' \
    # http://127.0.0.1:8000/mediacontent/ads/imageads/images/566d10ad1d41c8bd636ea654/
    def get(self, request, image_id):

        """ Returns a image identified by Id
         ---
         response_serializer: ImageContentSerializer
        """
        try:
#             auth_manager.do_auth(request)
            # Request Get, all users
            if request.method == 'GET':
                if image_id is not None:
                    img = ImageContent.objects.get(id=image_id)
                    return HttpResponse(img.image.read(),
                                        content_type="image/jpeg")
                return JSONResponse("", status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e), status=HTTP_401_UNAUTHORIZED)


class JpegImageViewSet(APIView):
    """ Returns JPEG Image resource """

    serializer_class = JpegImageContentSerializer
    model = JpegImageContent

    # curl -X GET -S -H 'Accept: application/json' \
    # http://127.0.0.1:8000/mediacontent/images/566d10ad1d41c8bd636ea654/
    def get(self, request, image_id):

        """ Returns a image identified by Id
         ---
         response_serializer: JpegImageContentSerializer
        """
        try:
#             auth_manager.do_auth(request)
            # Request Get, all users
            if request.method == 'GET':
                if image_id is not None:
                    img = JpegImageContent.objects.get(id=image_id)
                    return HttpResponse(img.image.read(),
                                        content_type="image/jpeg")
                return JSONResponse("", status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e), status=HTTP_401_UNAUTHORIZED)


class ImageAdViewSet(AdViewSet):

    """ Print/Image Campaign resource """

    serializer_class = ImageAdSerializer
    model = ImageAd

    # curl -X GET -S -H 'Accept: application/json' \
    # http://127.0.0.1:8000/mediacontent/ads/imageads/566c580f1d41c8a69d0a063d/566d10ad1d41c8bd636ea654/
    def get(self, request, campaign_id=None, ad_id=None):

        """ Returns a list of image campaign ads
         ---
         response_serializer: ImageAdSerializer
        """
        try:
            # Get all image-ads
            if campaign_id is None:
                ads = ImageAd.objects.all()
                serializer = ImageAdSerializer(ads, many=True)
                return JSONResponse(serializer.data)

            # Get more specific ads by campaigns
            camp = Campaign.objects.get(id=campaign_id)
            if ad_id is None:
                ads = ImageAd.objects.filter(campaign=camp)
                serializer = ImageAdSerializer(ads, many=True)
            else:
                ad = ImageAd.objects.get(id=ad_id)
                if ad.campaign.id == camp.id:
                    serializer = ImageAdSerializer(ad)
            return JSONResponse(serializer.data)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e), status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e), status=HTTP_401_UNAUTHORIZED)

    def _update(self, request, ad):

        try:
            # partial updates
            serializer = ImageAdSerializer(
                                data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                updated_obj = serializer.update(ad,
                                                serializer.validated_data)
                # Other reference fields
                # Store image'
                print '1'
                if "image" in request.data:
                    imageserializer = ImageContentSerializer(
                            data=request.data)
                    if imageserializer.is_valid(raise_exception=True):
                        img = imageserializer.save()
                        img_url = img.get_absolute_url()
                        updated_obj.update(image_content=img,
                                           image_url=img_url)
                print '2'
                if "offerex" in request.data:
                    #
                    #
                    #
                    #
                    # Extensions are stored and updated
                    offer = OfferExtensionSerializer(data=request.data['offerex'],
                                                     partial=True,
                                                     many=True)
                    if offer.is_valid(raise_exception=True):
                        ofs = offer.save()
                        updated_obj.update(offerex=ofs)
                print '3'
                if "socialex" in request.data:
                    #
                    #
                    #
                    #
                    # Extensions are stored and updated
                    social = SocialMediaExtensionSerializer(data=request.data['socialex'],
                                                            partial=True,
                                                            many=True)
                    if social.is_valid(raise_exception=True):
                        s_exs = social.save()
                        updated_obj.update(socialex=s_exs)
                print '4'
                updated_obj.save()
                return JSONResponse(str(updated_obj.id),
                                    status=HTTP_202_ACCEPTED)
            print '5'
            # Bad request
            return JSONResponse(str(serializer.errors),
                                status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return JSONResponse(str(e),
                                status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, campaign_id, ad_id=None):

        """ Creates an image ad for a campaign
         ---
         request_serializer: ImageAdSerializer
         response_serializer: ImageAdSerializer
        """

        # curl -X POST -S -H 'Accept: application/json'\
        # -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"\
        # http://127.0.0.1:8000/mediacontent/ads/imageads/566c580f1d41c8a69d0a063d/

        # Request put an Image Ad for already created
        # campaign
        try:
            auth_manager.do_auth(request)
            camp = Campaign.objects.get(id=campaign_id)
            if camp:
                # Check if an update is triggered
                if ad_id is not None:
                    ad = ImageAd.objects.get(id=ad_id)
                    return self._update(request, ad)

                img = None
                img_url = None
                offer = None
                social = None
                # Store image'
                if "image" in request.data:
                    imageserializer = ImageContentSerializer(
                            data=request.data["image"])
                    if imageserializer.is_valid(raise_exception=True):
                        img = imageserializer.save()
                        img_url = img.get_absolute_url()
                serializer = ImageAdSerializer(
                                data=request.data)
                if serializer.is_valid(raise_exception=True):
                    # Add other elements
                    if "offerex" in request.data:
                        #
                        #
                        #
                        #
                        # Extensions are stored and updated
                        offer = OfferExtensionSerializer(data=request.data["offerex"],
                                                         many=True)
                        if offer.is_valid(raise_exception=True):
                            offer = offer.save()
                    if "socialex" in request.data:
                        #
                        #
                        #
                        #
                        # Extensions are stored and updated
                        s_ex = SocialMediaExtensionSerializer(data=request.data["socialex"],
                                                              many=True)
                        if s_ex.is_valid(raise_exception=True):
                            social = s_ex.save()

                    ad = serializer.save(image_content=img,
                                         image_url=img_url)
                    ad.update(offerex=offer,
                              socialex=social,
                              campaign=camp)
                    # Successful
                    return JSONResponse(str(ad.id),
                                        status=HTTP_201_CREATED)
                return JSONResponse("Unknown error processing %s (%s) ." % (
                                            campaign_id, serializer.errors),
                                    status=HTTP_400_BAD_REQUEST)
        except DoesNotExist as e:
            print e
            return JSONResponse(str(e), status=HTTP_404_NOT_FOUND)
        except UserNotAuthorizedException as e:
            print e
            return JSONResponse(str(e), status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print e
            return JSONResponse("Campaign with Id (%s) not found." % campaign_id,
                                status=HTTP_404_NOT_FOUND)

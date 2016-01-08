from userapp.JSONFormatter import JSONResponse
from rest_framework.views import APIView
from mediacontentapp.serializers import AdSerializer, TextAdSerializer,\
    CallOnlyAdSerializer, ImageAdSerializer, CampaignSerializer,\
    ImageContentSerializer
from userapp.models import MediaUser
from mediacontentapp.models import Ad, TextAd, CallOnlyAd, ImageAd, Campaign,\
    ImageContent
from mediacontentapp.controller import CampaignManager
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK
from datetime import date, datetime
from PIL import Image
from django.http.response import HttpResponse
from django.utils.baseconv import base64
import base64


class CampaignViewSet(APIView):

    """ campaign resource """

    serializer_class = CampaignSerializer
    model = Campaign
    # View controller
    controller = CampaignManager()

    def get(self, request, username):

        """ Returns a list of campaigns for a user
         ---
         response_serializer: CampaignSerializer
        """
        if username:
            user = MediaUser.objects.get(username=username)
            cs = Campaign.objects.filter(creator=user)
            serializer = CampaignSerializer(cs, many=True)
            return JSONResponse(serializer.data)

    def post(self, request, username):

        """ Creates a campaign for a user
         ---
         request_serializer: CampaignSerializer
         response_serializer: CampaignSerializer
        """
        try:
            if username:
                create_time = datetime.now()
                user = MediaUser.objects.get(username=username)
                if user:
                    serializer = CampaignSerializer(
                                                data=request.data)
                    if serializer.is_valid():
                        campaign = serializer.save(creation_time=create_time,
                                                   creator=user)
                        # Prepare the campaign for the User
                        self.controller.prepare_campaign(
                                                    user_id=user,
                                                    args=campaign)
                        return JSONResponse(serializer.data,
                                            status=HTTP_201_CREATED)
            else:
                return JSONResponse(serializer.errors,
                                    status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return JSONResponse(serializer.errors,
                                status=HTTP_500_INTERNAL_SERVER_ERROR)


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
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
                else:
                    return JSONResponse(serializer.errors,
                                        status=HTTP_400_BAD_REQUEST)
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
        # Request Get, all users
        if request.method == 'GET':
            ads = CallOnlyAd.objects.all()
            serializer = CallOnlyAdSerializer(ads, many=True)
            return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):

        """ Creates a Call only campaign Ad
         ---
         request_serializer: CallOnlyAdSerializer
         response_serializer: CallOnlyAdSerializer
        """
        # Request Post, create user
        if request.method == 'POST':
            try:
                serializer = CallOnlyAdSerializer(data=request.data)
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
        # Request Get, all users
        if request.method == 'GET':
            if image_id is not None:
                img = ImageContent.objects.get(id=image_id)
                return HttpResponse(img.image.read(),
                                    content_type="image/jpeg")
            return JSONResponse("", status=HTTP_404_NOT_FOUND)


class ImageAdViewSet(AdViewSet):

    """ Print/Image Campaign resource """

    serializer_class = ImageAdSerializer
    model = ImageAd

    # curl -X GET -S -H 'Accept: application/json' \
    # http://127.0.0.1:8000/mediacontent/ads/imageads/566c580f1d41c8a69d0a063d/566d10ad1d41c8bd636ea654/
    def get(self, request, campaign_id, ad_id=None):

        """ Returns a list of image campaign ads
         ---
         response_serializer: ImageAdSerializer
        """
        # Request Get, all users
        if request.method == 'GET':
            camp = Campaign.objects.get(id=campaign_id)
            if ad_id is None:
                ads = ImageAd.objects.filter(campaign=camp)
                serializer = ImageAdSerializer(ads, many=True)
            else:
                ad = ImageAd.objects.get(id=ad_id)
                if ad.campaign.id == camp.id:
                    serializer = ImageAdSerializer(ad)
            return JSONResponse(serializer.data)

    def post(self, request, campaign_id):

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
        if request.method == 'POST':
            camp = Campaign.objects.get(id=campaign_id)
            if camp:
                # Store image'
                imageserializer = ImageContentSerializer(
                        data=request.data)
                if imageserializer.is_valid():
                    img = imageserializer.save()

                serializer = ImageAdSerializer(
                                data=request.data)
                if serializer.is_valid():
                    serializer.save(campaign=camp, image_content=img,
                                    image_url=img.get_absolute_url())
                    return JSONResponse(serializer.data,
                                        status=HTTP_201_CREATED)
        return JSONResponse(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)

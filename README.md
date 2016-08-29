# README #

This README documents the steps that are necessary to get your AdWise application up and running.

### What is this repository for? ###

* Quick summary
AdWise system comprises of User management application, Mediacontent management application and Advertisement analytics related applications.
In future other relevant application will be added.

* Version
0.1.01 master

* Branch
remotes/origin/adwise-userprofile-mgr_0.1_patch1

### How do I get the dev set up? ###

* Summary of set up
Eclipse IDE is recommended. And all the source code is in Python 2.7 with PEP8 checks.
* Configuration
Python 2.7
* Dependencies
Python dependencies are the following 

* Django==1.6.11
* Pillow==3.0.0
* PyYAML==3.11
* amqp==1.4.8
* anyjson==0.3.3
* argparse==1.2.1
* billiard==3.3.0.22
* blinker==1.4
* celery==3.1.19
* django-mongodb-engine==0.6.0
* django-rest-framework-mongoengine==2.0.2
* django-rest-swagger==0.3.4
* djangorestframework==3.2.4
* djangotoolbox==1.8.0
* kombu==3.0.32
* mongoengine==0.10.0
* pymongo==3.0.3
* pytz==2015.7
* wsgiref==0.1.2

OS System components are 

* MONGODB  
* sudo apt-get install libjpeg8-dev zlib1g-dev
* sudo apt-get install rabbitmq-server
* Download and install elastic search from http://www.elastic.co/downloads
* Install celery

* Database configuration
This project uses MONGODB.

* How to run tests
python manage.py tests

* Deployment instructions
* Create a Virtual environment project.
* Activate the environment by running, <projectfolder>/bin/activate.
    It should give you a prompt like 
   (project_name)user@ubuntu:>
* git clone git@bitbucket.org:adwise-m/adwise-userprofile-mgr.git
* pip install -r requirements.txt
* Install MONGODB using sudo apt-get, get the latest.
* Perform, sudo apt-get install libjpeg8-dev zlib1g-dev
* Perform, sudo apt-get install rabbitmq-server
* Start the AdWise server using the command,
    (project_name)user@ubuntu:> python manage.py runserver.
* To verify everything is fine open Browser,
    http://127.0.0.1:8000/ 
    should display the swagger API page.
    

### Contribution guidelines ###
To be drafted.

### Who do I talk to? ###

series-5

### API Reference ###

Most of the API(s) are documented correctly in Swagger UI, which is 
available in the home-page (http://127.0.0.1:8000/).
Please refer swagger to understand the API schema.

Note: Here are few examples of using the REST API(s). Where-ever instance GUIDs
replace it with the real GUIDs in your system.

# Create a service User
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "user": {"name": "serviceuser", "username": "serviceuser@series-5.com","password":"adwise123","address": "TBD","city":"Bangalore","state":"Karnataka","point": [0.0, 0.0], "phone_number":"9880563410", "email":"serviceuser@series-5.com", "gender": "Male", "pin": "560048"}}' http://localhost:8000/users/

# Create a demo User
sudo curl -H "Content-Type: application/json" -H "username:demouser@series-5.com" -H "password:demo123" -H "email:demouser@series-5.com" -X POST -d '{ "user": { "name": "demouser", "username": "demouser@series-5.com","password":"demo123","address": "TBD","city":"Bangalore","state":"Karnataka","point": [0.0, 0.0], "phone_number":"9880563410", "email":"demouser@series-5.com", "gender": "Male", "pin": "560048"}}' http://localhost:8000/users/

# Create agency/project and a user together
 sudo curl -H "Content-Type: application/json" -H "username:lion4" -H "password:lion1234" -H "email:lion4@jungle.com" -X POST -d '{ "user": {"username": "lion4","password":"lion1234","address": "742 Evergreen Terrace","city":"Springfield","state":"Oregon","point": [-123.0208, 44.0464], "phone_number":"roar", "email":"lion4@jungle.com", "gender": "Male", "pin": "560077"}, "project": {"name": "somename", "type": "Media Agency", "address": "somelocation", "city": "Bangalore", "state": "Karnataka", "pin":"560077"}, "role" : {"name":"r1"}}' http://localhost:8000/users/

# Create agency/project, preferences and a user - all in one command.
sudo curl -H "Content-Type: application/json" -H "username:sonu@series-5.com" -H "password:sonu123" -H "email:sonu@series-5.com" -X POST -d '{ "user": {"name": "sonu", "username": "sonu@series-5.com","password":"sonu123","address": "742 Evergreen Terrace","city":"Springfield","state":"Oregon","point": [-123.0208, 44.0464], "phone_number":"9880563410", "email":"sonu@series-5.com", "gender": "Male", "pin": "560077"}, "project": {"name": "somename", "type": "Media Agency", "address": "somelocation", "city": "Bangalore", "state": "Karnataka", "pin":"560077"}, "role" : {"name":"r1"}, "device_pref": [{"device_tag": "tag1", "device_type": "tab", "device_info": {}}, {"device_tag": "tag1", "device_type": "tab", "device_info": {"a":"b"}}], "loc_pref": [{"location_name": "work", "loc": [0.0, 2.0]}], "personal_pref": [{"personal_name":"pref1", "value": "value1", "personal_info": {"c":"d"}}], "media_pref": [{"media_tag":"tag1", "media_type":"leisure", "media_info":{"e":"f"}}]}' http://localhost:8000/users/

# Get a previous known user by Id

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Content-Type: application/json" -H "username:sonu1@series-5.com" -H "password:sonu123" -H "email:sonu1@series-5.com" -X GET http://127.0.0.1:8000/users/$object-id/

where $object_id is the Id, you get when you had created the user first time.


# Login user
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/users/login/

# Create a OOH media source as a service User
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/sc.jpg;type=image/jpg" -F "name"="kundanahalli_40x40" -F "type"="ooh" -F "street_name"="kundanahalli railway gate" -F "city"="Bangalore" -F "state"="Karnataka" -F "country"="India" -F "pin"="560057"  http://127.0.0.1:8000/mediacontent/mediasource/ooh/ 

# Update OOH instance by its Id
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "city"="Bengaluru" -F "state"="Karnataka" -F "country"="India" -F "pin"="560057"  http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Update OOH instance for its Booking
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "booking" : { "start_time" : "2016-02-25T18:37:21.766000", "duration" : 10, "type" : "commercial"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Update OOH instance for its Pricing
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "pricing" : { "name" : "festival", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Update OOH instance attributes and the owner by Id (transferring ownership) - user Id, is the username of new owner
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "city"="New Delhi" -F "state"="Delhi"  http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/?userid=demouser@series-5.com

# Update (All-in-One) Pricing + Booking + Attributes
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "city" : "Chennai", "state" : "Tamil Nadu", "country" : "India", "pricing" : { "name" : "diwali", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000"}, "booking" : { "start_time" : "2016-02-25T18:37:21.766000", "duration" : 10, "type" : "educational"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Get a OOH instance by id
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:8000/mediacontent/mediasource/ooh/?id=56b5f4ca1d41c85e256e11c2

# Get a OOH instance owned by a User (by Username)
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:8000/mediacontent/mediasource/ooh/?userid=serviceuser@series-5.com

# Create OOH (all properties except image)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "kundanahalli_40x40", "type" : "ooh", "street_name" : "kundanahalli railway gate", "city" : "Bangalore", "state" : "Karnataka", "country" : "India", "point": [124.78, 32.0], "size": [10, 4], "pin" : "560057", "pricing" : { "name" : "diwali", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000"}, "booking" : { "start_time" : "2016-02-25T18:37:21.766000", "duration" : 10, "type" : "educational"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/

# Create OOH
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "kundanahalli_40x40", "type" : "ooh", "street_name" : "kundanahalli railway gate", "city" : "Bangalore", "state" : "Karnataka", "country" : "India", "point": [124.78, 32.0], "size": [10, 4], "pin" : "560057", "pricing" : { "name" : "diwali", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000"}, "booking" : { "start_time" : "2016-02-25T18:37:21.766000", "duration" : 10, "type" : "educational"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/

# Update image for OOH
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Create MediaAggregates
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "Inorbit", "display_name" : "InOrbit Whitefield", "survey_name" : "No. 75", "address1": "EPIP Area", "address2": "Whitefield", "city": "Bangalore Bengaluru", "state": "Karnataka", "country": "India", "pin": "560066", "location": [17.4410, 78.3921], "poi_marker_data": {"a":"b"}, "internet_settings": {"home_url": "http://inorbit.in/whitefield/"}, "type": "ShoppingMall"}' http://127.0.0.1:8000/mediacontent/mediaaggregates/

# Update MediaAggregates to upload Images (icon and image)
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image_content=@/home/sonu/adimages/malls/inorbit.png;type=image/png" -F "icon_content=@/home/sonu/adimages/malls/inorbit_icon.png;type=image/png" http://127.0.0.1:8000/mediacontent/mediaaggregates/57c1d8571d41c87129ed53bf/

# Add additional sources to MediaAggregates

# Get MediaAggregates
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediaaggregates/

# Get MediaAggregate types
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://172.31.41.248:8000/mediacontent/mediaaggregates/types/

# Creating/Updating a dashboard for the User - set approriate dashboard type. (Media Agency - "MA", Billboard Owner - "BO", On baording partner -> "Partner", Service User -> "Unknown")
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"dashboard_type":"MA"}' http://127.0.0.1:8000/mediacontent/dashboard/

# Getting a dashboard for the User
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/dashboard/

# Storing a share/like/dislike request by Billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST  -d '{"activity_meta" : "email=sonu@g.com, phone=ksksk"}' http://localhost:8000/mediacontent/mediasource/activity/share/56c0b94c1d41c8957cba8237

# Fetching a share/like/dislike activity by billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/mediasource/activity/share/56c0b94c1d41c8957cba8237

# Adding tags to a billboard, E.g adds nearby tag with values school and temple.
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name":"nearby", "tags": ["school", "temple"], "type":1.0}'  http://localhost:8000/mediacontent/mediasource/tags/56c0b94c1d41c8957cba8237

# Getting added tags to a billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/mediasource/tags/56c0b94c1d41c8957cba8237

# Miscellaneous
# Create a service called 'location' for the User
sudo curl -H "Content-Type: application/json" -X POST -d '{"target_service_name": "location", "service_meta": "empty"}' http://localhost:8000/users/services/lion2/location/

# Create a campaign
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "P(x) campaign", "description": "Starters T20", "launched_at": "2016-04-25T18:37:21.766000", "end_at": "2016-04-29T18:37:21.766000", "target_group":[], "linked_source_ids":["56f75d6f1d41c81380d87b65"], "spec" :{"name":"basic", "type": "basictype", "ad_type":"imagead"}}' http://localhost:8000/mediacontent/campaign/

Note: ad_type value can be used to fetch the ad content for this campaign
For example, /mediacontent/ads/<$ad_type>/<$campaign_id>

sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "IPL World T20", "description": "IPL T20 cricket championship", "launched_at": "2016-04-25T18:37:21.766000", "end_at": "2016-04-29T18:37:21.766000", "tags": "cricket football golf", "category": "sports", "city": ["bengaluru", "delhi"], "state": ["karnantaka","Delhi"], "spec" :{"name":"basic", "type": "basictype", "ad_type":"imagead"}}' http://localhost:8000/mediacontent/campaign/

# Get all campaigns for the User
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/campaign/

# Update a campaign
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "P(x1) campaign", "description": "Starters T20", "launched_at": "2016-04-25T18:37:21.766000", "end_at": "2016-04-29T18:37:21.766000", "spec" :{"name":"basic1", "type": "basictype", "ad_type":"imagead", "target_group":[], "linked_source_ids":["56f75d6f1d41c81380d87b65","56f76fc01d41c81fe5ac9cd9"]}}' http://localhost:8000/mediacontent/campaign/56f76fc01d41c81fe5ac9cd9/

# Update home page image for a campaign
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" http://localhost:8000/mediacontent/campaign/570746dd1d41c84bc448786b/

# Create an ImageAd for a campaign
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" -F "display_url"="http://hp.com" -F "final_urls"="http://hp.com" -F "mobile_urls"="http://hp.com" -F "app_urls"="http://hp.com" -F "thirdparty_tracking_url"="http://track.com" -F "adwise_tracking_url"="http://hp.com" -F "ad_type"="ImageAd" http://127.0.0.1:8000/mediacontent/ads/imageads/5677bbb31d41c84312e9cd91/

Format is, /mediacontent/ads/imageads/<$campaign_id>

# Get all ImageAd(s) by a campaign
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/ads/imageads/570012561d41c86ca6e79d6b/

Format is, /mediacontent/ads/imageads/<$campaign-id>/

# Get a specific instance of ImageAd
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/ads/imageads/570012561d41c86ca6e79d6b/570015fe1d41c86ca6e79d71/

Format is, /mediacontent/ads/imageads/<$campaign_id>/<$imagead_id>

# Add ImageAd with offer extension
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"offerex":[{"ex_name": "new customer offer", "ex_type": "offer", "offer_code": "QOWGX", "offer_description": "pre-launch offer", "openDay":"2016-04-29T18:37:21.766000", "closeDay": "2016-04-29T18:37:21.766000"}]}' http://localhost:8000/mediacontent/ads/imageads/57002fb11d41c8855868dbd4/570739611d41c84309e0a976/

# Add ImageAd with all attributes except for Image itself.

sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"display_url":"http://hp.com","final_urls":"http://hp.com","mobile_urls":"http://hp.com","app_urls":"http://hp.com","thirdparty_tracking_url":"http://track.com", "adwise_tracking_url":"http://hp.com","ad_type":"ImageAd","offerex":[{"ex_name": "new customer offer", "ex_type": "offer", "offer_code": "QOWGX", "offer_description": "pre-launch offer", "openDay":"2016-04-29T18:37:21.766000", "closeDay": "2016-04-29T18:37:21.766000"}], "socialex":[{"socialmedia_type":"facebook", "socialmedia_url":"http://facebook.com/series-5.com", "socialmedia_headline": "facebook free basic campaign"}, {"socialmedia_type":"twitter", "socialmedia_url":"http://twitter.com/series-5.com", "socialmedia_headline": "twitter free basic campaign"}]}' http://localhost:8000/mediacontent/ads/imageads/571a72741d41c8b297ff2e75/

# Add Image to an ImageAd
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" http://127.0.0.1:8000/mediacontent/ads/imageads/571a72741d41c8b297ff2e75/572704641d41c8e673f4848d/

# Do a research
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "helmet", "query_type": "multifield", "query_object_type": "Campaign", "query_fields":{"category":4, "description":2}}' http://127.0.0.1:8000/research/search/

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "hel.*", "query_type": "regexp", "query_object_type": "Campaign", "query_fields":{"category":4}}' http://127.0.0.1:8000/research/search/

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "helmet"}' http://127.0.0.1:8000/research/search/

# Invoking search API internally, doesn't do any user validations.
curl -H "Content-Type: application/json" -X POST -d '{"raw_strings": "fitness", "query_type": "OOHMediaSource", "query_fields":{"category":4, "description":2}}' http://127.0.0.1:8000/research/query/

# Submitting OOH operational data for analytics (Bulk upload)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '[{"visitor_total_count":170000, "breakups": {"age":{"15-20": 100, "20-28": 200, "28-35": 500}, "commute":{"bus":500,"cabs": 1200,"cars": 1500}, "target":{"profs":1200, "teens":5000, "biz":5000}}, "feed_timestamp":"2016-06-01T18:37:21.766000"}, {"visitor_total_count":3500, "breakups": {"age":{"15-20": 100, "20-28": 200, "28-35": 500}, "commute":{"bus":500,"cabs": 1200,"cars": 1500}, "target":{"profs":1200, "teens":5000, "biz":5000}}, "feed_timestamp":"2016-06-02T18:37:21.766000"}]' http://127.0.0.1:8000/mediacontent/etl/ooh/574d68571d41c8ba3f289e84/

# Submitting OOH operational data for analytics (One sample)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '[{"visitor_total_count":170000, "breakups": {"age":{"15-20": 100, "20-28": 200, "28-35": 500}, "commute":{"bus":500,"cabs": 1200,"cars": 1500}, "target":{"profs":1200, "teens":5000, "biz":5000}}, "feed_timestamp":"2016-06-01T18:37:21.766000"}]' http://127.0.0.1:8000/mediacontent/etl/ooh/574d68571d41c8ba3f289e84/


Template: http://<localhost>:8000/mediacontent/etl/ooh/<ooh_instance_id>/
# Tools
# Tool for creating campaign
python ./campaign_import.py tabseparated_camp.data http://127.0.0.1:8000 /home/sonu/adimages/campaigns/
# Tool for importing Ads to a campaign
python ./ad_import.py tabseparated_ad.data http://127.0.0.1:8000 /home/sonu/adimages/campaigns/ 570746dd1d41c84bc448786b

# __END__

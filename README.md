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

* sudo apt-get install mongdb
* sudo apt-get install libjpeg-dev zlib1g-dev
* sudo apt-get install python-dev
* sudo apt-get install gcc
* git clone https://sudhakso@bitbucket.org/adwise-m/adwise-userprofile-mgr.git
* pip install -r requirements.txt
* pip uninstall django-rest-framework-mongoengine
* pip uninstall django-rest-framework-mongoengine==3.3.0
* sudo apt-get install rabbitmq-server
* Install JAVA
	sudo add-apt-repository ppa:openjdk-r/ppa  
	sudo apt-get update   
	sudo apt-get install openjdk-7-jdk 
* Get elasticsearch
	mkdir /home/ubuntu/tools
	cd /home/ubuntu/tools
	wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.3.1/elasticsearch-2.3.1.tar.gz
	tar -xvf elasticsearch-2.3.1.tar.gz
* Modify the $ADWISE_REPO/tools/startall.sh to adjust to your paths and run.
	

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
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/mediasource/ooh/?id=56b5f4ca1d41c85e256e11c2

# Get a OOH instance owned by a User (by Username)
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/mediasource/ooh/?userid=serviceuser@series-5.com

# Create OOH (all properties except image)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "kundanahalli_40x40", "type" : "ooh", "street_name" : "kundanahalli railway gate", "city" : "Bangalore", "state" : "Karnataka", "country" : "India", "point": [124.78, 32.0], "size": [10, 4], "pin" : "560057", "pricing" : { "name" : "diwali", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000"}, "booking" : { "start_time" : "2016-02-25T18:37:21.766000", "duration" : 10, "type" : "educational"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/

# Create OOH
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "kundanahalli_40x40", "type" : "ooh", "street_name" : "kundanahalli railway gate", "city" : "Bangalore", "state" : "Karnataka", "country" : "India", "point": [124.78, 32.0], "size": [10, 4], "pin" : "560057", "pricing" : { "name" : "diwali", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000"}, "booking" : { "start_time" : "2016-02-25T18:37:21.766000", "duration" : 10, "type" : "educational"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/

# Update image for OOH
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Trigger discovery of Amenities near a given OOH
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST http://127.0.0.1:8000/mediacontent/mediasource/nearby/ooh/584cf2621d41c8d2d5a04a75/

# Get amenities near the OOH
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediasource/nearby/ooh/584cf2621d41c8d2d5a04a75/


# Create MediaAggregates
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "Inorbit", "display_name" : "InOrbit Whitefield", "survey_name" : "No. 75", "address1": "EPIP Area", "address2": "Whitefield", "city": "Bangalore Bengaluru", "state": "Karnataka", "country": "India", "pin": "560066", "location": [17.4410, 78.3921], "poi_marker_data": {"a":"b"}, "internet_settings": {"home_url": "http://inorbit.in/whitefield/"}, "type": "ShoppingMall"}' http://127.0.0.1:8000/mediacontent/mediaaggregates/

# Update MediaAggregates to upload Images (icon and image)
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image_content=@/home/sonu/adimages/malls/inorbit.png;type=image/png" -F "icon_content=@/home/sonu/adimages/malls/inorbit_icon.png;type=image/png" http://127.0.0.1:8000/mediacontent/mediaaggregates/57c2e250c0c9542b3f5ca393/

# Add additional sources to MediaAggregates

# Get MediaAggregates
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediaaggregates/?myowned=True

# Get MediaAggregates by a given type
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://172.31.41.248:8000/mediacontent/mediaaggregates/?typename=<$typename>

# Get MediaAggregate types
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://172.31.41.248:8000/mediacontent/mediaaggregates/types/

##### Extension Related APIs
This section covers the APIs used to create/update/link extension objects.

# Add amenity extensions to the MediaAggregate
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' http://127.0.0.1:8000/mediacontent/mediaaggregates/<$aggregate-id>/extensions/?"ids=bc&ids=de&ids=fg"
# 57d844351d41c87ef6affad9

# Get all extensions of a MediaAggregate
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediaaggregates/57f0e9bec0c9544a6dc8537f/extensions/

# Get all extensions by a given type available in a MediaAggregate
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediaaggregates/57d844351d41c87ef6affad9/extensions/retail/

# Create or update amenity extension
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"valid_from":"2016-02-25T18:37:21.766000", "category": "shopping", "tagwords": "discount shopee", "outlet_name": "somename", "outlet_description":"some desc", "outlet_address1": "Addr1", "outlet_address2":"addr2", "affliations": "parent brand", "outlet_url": "http://someurl.com", "brands": "nike puma adidas"}' http://127.0.0.1:8000/mediacontent/extension/amenity/retail/$extension-id/

where extension-name is retail in this example,
      extension-id is the id of the extension to update 

sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"valid_from":"2016-02-25T18:37:21.766000", "category": "shopping", "tagwords": "discount shopee", "brand_name": "somename", "brand_description": "some desc", "brand_url": "http://nike.com"}' http://127.0.0.1:8000/mediacontent/extension/amenity/brand/$extension-id/

sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"valid_from":"2016-02-25T18:37:21.766000", "category": "shopping", "tagwords": "discount shopee", "outlet_name": "somename", "outlet_description": "some desc", "outlet_address1": "addr1", "outlet_address2": "addr2", "cusine": "chineese", "outlet_type": "bar", "average_price_for_2": "200 rs", "smoking_allowed": "False", "beverages_served": "True", "outlet_url": "http://bar.com"}' http://127.0.0.1:8000/mediacontent/extension/amenity/fnb/$extension-id/

# Add advensturesport
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"valid_from":"2016-02-25T18:37:21.766000", "category": "park", "tagwords": "holiday entertainment adventure vacation", "brand_name": "Waynad BioGarden", "brand_description": "A unique nature based multi theme park is WBG put in one sentence. A perfect harmonious relation shared between man and nature is the main aspect making WBG a unique attraction in Kerala. Located amidst the misty hills of Wayanad, WBG is a perfect get away to unwind and relax at the heart of Mother Nature.", "brand_url":"http://wayanadbiogarden.org/the-park/", "outlet_address1": "Wayanad Bio Garden WGGI - LLP TP III/346C,Cheepad,Makkiyad P.O", "outlet_address2":"Kerala", "sport_name":"Water Ride", "sport_description":"Backwaters of Kerala", "capacity":"1500 units", "target_age_group":"20-35, 50-65","brand_partners":["Playzone Inc.", "Playful Event services"], "service_condition":"Water sport can be availaed only wearing safety gears","reservation_facility":"True","average_price":"15000 pp","open_days":"Friday Only", "open_timings":"6:00AM-5:00PM"}' http://ec2-52-10-208-37.us-west-2.compute.amazonaws.com:8000/mediacontent/extension/amenity/adventuresport/

# Add movie multiplex
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"valid_from":"2016-02-25T18:37:21.766000", "category": "moviemultiplex", "tagwords": "movie entertainement fun", "brand_name": "PVR Cinemas", "brand_description": "PVR Is The Largest And The Most Premium Film And Retail Entertainment Company In India. Since Its Inception In 1997, The Brand Has Redefined The Way Entertainment Is Consumed In India. It Currently Operates A Cinema Circuit Comprising Of 569 Screens In 123 Properties In 48 Cities Pan India.", "brand_url":"https://www.pvrcinemas.com/", "outlet_address1": "PVR Head", "outlet_address2":"Bangalore", "audis":"10", "capacity_per_audi":"125","service_condition":"Water sport can be availaed only wearing safety gears","reservation_facility":"True", "reservation_number":"918023688570", "reservation_url":"http://bookmyshow.com","average_price":"15000 pp","open_days":"Friday Only", "show_timings":["6:00AM-5:00PM"], "common_name:": "Movies"}' http://ec2-52-10-208-37.us-west-2.compute.amazonaws.com:8000/mediacontent/extension/amenity/moviemultiplex/

# Add image to an existing extension
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" http://localhost:8000/mediacontent/extension/amenity/<$extension-name>/<$extension-id>/

# Get an existing extension by its Id
curl -X GET -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" http://localhost:8000/mediacontent/extension/amenity/<$extension-name>/<$extension-id>/


##### API to attach a Campaign to OOHMediasource
# API to attach a campaign to a OOHMediaSource
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"start_date" : "2016-02-25T18:37:21.766000","end_date" :"2016-02-25T18:37:21.766000"}' "http://127.0.0.1:8000/mediacontent/mediasource/ooh/57d844351d41c87ef6affad9/?action=addcontent&id=57c062201d41c83e549e8ae5"

The query format is,
/mediacontent/mediasource/ooh/$ooh_id/?action=addcontent&id=$campaign_id"

#API to query campaign

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/playing/oohmediasource/?"id=58c4f5931d41c828ff8bc6dc"

# API to pause and resume content
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediasource/ooh/5928f7ca1d41c885656a92f2/?action=pausecontent&id=57c0621e1d41c83e549e8ae0"

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediasource/ooh/5928f7ca1d41c885656a92f2/?action=resumecontent&id=57c0621e1d41c83e549e8ae0"


curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediasource/venue/5928f7ca1d41c885656a92f2/?action=resumecontent&id=57c0621e1d41c83e549e8ae0"

##### API to attach a Campaign to MediaAggregate
# API to attach a campaign to a MediaAggregate
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"start_date" : "2016-02-25T18:37:21.766000","end_date" :"2016-02-25T18:37:21.766000"}' "http://127.0.0.1:8000/mediacontent/mediaaggregates/57d844351d41c87ef6affad9/?action=addcontent&id=57c062201d41c83e549e8ae5"

The query format is,
/mediacontent/mediaaggregates/$aggregate_id/?action=addcontent&id=$campaign_id"

# API to query campaigns attached to a MediaAggregate that are Valid (campaign beyond expiry date is not returned)
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/playing/mediaagregate/?"id=58c4f5931d41c828ff8bc6dc"

The query format is,
/mediacontent/playing/mediaagregate/?id=$aggregate_id

# Pause a campaing
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediaaggregates/5928f5b11d41c883096fde9b/?action=pausecontent&id=57c0621e1d41c83e549e8ae0"

The query format is,
/mediacontent/mediaaggregates/$aggregate_id/?action=pausecontent&id=$campaign_id"

# Resume a campaing
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediaaggregates/5928f5b11d41c883096fde9b/?action=resumecontent&id=57c0621e1d41c83e549e8ae0"

The query format is,
/mediacontent/mediaaggregates/$aggregate_id/?action=resumecontent&id=$campaign_id"


# API to query all campaigns (inlcuding expired ones) attached to a MediaAggregate
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/playing/mediaagregate/?"id=58c4f5931d41c828ff8bc6dc&all"


# Creating/Updating a dashboard for the User - set approriate dashboard type. (Media Agency - "MA", Billboard Owner - "BO", On baording partner -> "Partner", Service User -> "Unknown")
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"dashboard_type":"MA"}' http://127.0.0.1:8000/mediacontent/dashboard/

# Getting a dashboard for the User
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/dashboard/

# Storing a share/like/dislike request by Billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST  -d '{"activity_meta" : "email=sonu@g.com, phone=ksksk"}' http://localhost:8000/mediacontent/mediasource/activity/share/56c0b94c1d41c8957cba8237

# Storing an activity on a mediaaggregate
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST  -d '{"activity_data" : {"message":"somedata", "sharingtype":"gmail"}}' http://localhost:8000/mediacontent/mediaaggregate/activity/share/56c0b94c1d41c8957cba8237/

Following activities are supported, 'share', 'like', 'dislike', 'quote', 'view'

# Storing an activity on a campaign
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST  -d '{"activity_data" : {"message":"somedata", "sharingtype":"gmail"}}' http://localhost:8000/mediacontent/activity/campaign/share/56c0b94c1d41c8957cba8237/

# storing an activity on a Ad
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST  -d '{"activity_data" : {"message":"somedata", "sharingtype":"gmail"}}' http://localhost:8000/mediacontent/activity/ad/share/56c0b94c1d41c8957cba8237/

# storing an activity on a Offer
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST  -d '{"activity_data" : {"message":"somedata", "sharingtype":"gmail"}}' http://localhost:8000/mediacontent/activity/offer/share/56c0b94c1d41c8957cba8237/

# Fetching a share/like/dislike activity by billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/mediasource/activity/share/56c0b94c1d41c8957cba8237

# Adding tags to a billboard, E.g adds nearby tag with values school and temple.
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name":"nearby", "tags": ["school", "temple"], "type":1.0}'  http://localhost:8000/mediacontent/mediasource/tags/56c0b94c1d41c8957cba8237

# Getting added tags to a billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/mediasource/tags/56c0b94c1d41c8957cba8237

# Miscellaneous - Service API (e.g. offers, notification, email etc.)
# Create a service subscription called 'location' for the User
sudo curl -H "Content-Type: application/json" -X POST -d '{"target_service_name": "location", "service_meta": "empty"}' http://localhost:8000/users/services/$user-id/location/

# Create a service subscription called 'notification' for the User
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' http://localhost:8000/users/services/$user-id/$service-friendly-name/

e.g. valid names are "location", "meter", "gcm", "notification", "offer", "event" etc.

# Create a service favourite for a User
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"service_meta": {"favourite_data": {"campaigns":[{"name":"somecamp", "idref":"585a15d61d41c8c90ada29b1", "image_url":"/content/image01"}], "aggregates":[{"name":"someaggregate", "idref":"585a15d61d41c8c90ada29b1", "image_url":"/content/agg01"}, {"name":"someaggregate", "idref":"585a15d61d41c8c90ada29b1", "image_url":"/content/agg01"}], "extensions":[{"name":"someext", "idref":"585a15d61d41c8c90ada29b1", "image_url":"/content/ext01"}], "offers":[{"name":"someoffer", "idref":"585a15d61d41c8c90ada29b1", "image_url":"/content/offer01"}, {"name":"someoffer", "idref":"585a15d61d41c8c90ada29b1", "image_url":"/content/offer01"}, {"name":"someoffer", "idref":"585a15d61d41c8c90ada29b1", "image_url":"/content/offer01"}]}}}' http://localhost:8000/users/services/$user-service-id/data/

# Get all the services availed for a User
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/users/services/$user-id/

# Get detail of a service by its friendly name
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/users/services/$user-id/notification/

e.g. service-friendly-name=notification

# Feed service data subscribed to the User by its service key
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"service_meta": {"notif_data": {"a":"b", "c":"Account running low balance"}, "notif_expiry_date":"2016-04-25T18:37:21.766000"}}' http://localhost:8000/users/services/$user-service-id/data/

# Get service data subscribed to the User by its service key
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET -d http://localhost:8000/users/services/$user-service-id/data/

for e.g. returns instances referred under service "58249eda1d41c8f79d19569d"
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/users/services/58249eda1d41c8f79d19569d/data/


# Create a campaign
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "P(x) campaign", "description": "Starters T20", "launched_at": "2016-04-25T18:37:21.766000", "end_at": "2016-04-29T18:37:21.766000", "target_group":[], "linked_source_ids":["56f75d6f1d41c81380d87b65"], "spec" :{"name":"basic", "type": "basictype", "ad_type":"imagead"}}' http://localhost:8000/mediacontent/campaign/

Note: ad_type value can be used to fetch the ad content for this campaign
For example, /mediacontent/ads/<$ad_type>/<$campaign_id>

sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "IPL World T20", "description": "IPL T20 cricket championship", "launched_at": "2016-04-25T18:37:21.766000", "end_at": "2016-04-29T18:37:21.766000", "tags": "cricket football golf", "social_url":"http://fb.com/ipl202017", "home_url": "http://ipl.com/", "category": "sports", "city": ["bengaluru", "delhi"], "state": ["karnantaka","Delhi"], "spec" :{"name":"basic", "type": "basictype", "ad_type":"imagead"}}' http://localhost:8000/mediacontent/campaign/

# Update campaign tracking
# updates a short url for the campaign
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "gp-2", "description": "gp flipkart offers", "language_code": "en"}' http://localhost:8000/mediacontent/campaign/59511ec71d41c8f7e82c0daf/track/


# Get all campaigns for the User
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/campaign/

# Update a campaign
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "P(x1) campaign", "description": "Starters T20", "launched_at": "2016-04-25T18:37:21.766000", "end_at": "2016-04-29T18:37:21.766000", "spec" :{"name":"basic1", "type": "basictype", "ad_type":"imagead", "target_group":[], "linked_source_ids":["56f75d6f1d41c81380d87b65","56f76fc01d41c81fe5ac9cd9"]}}' http://localhost:8000/mediacontent/campaign/56f76fc01d41c81fe5ac9cd9/

# get all sources where the campaign is played
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/campaign/playing/57c062201d41c83e549e8ae5/


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

sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"display_url":"http://hp.com","final_urls":"http://hp.com","mobile_urls":"http://hp.com","app_urls":"http://hp.com","thirdparty_tracking_url":"http://track.com", "adwise_tracking_url":"http://hp.com","ad_type":"ImageAd","offerex":[{"ex_name": "new customer offer", "ex_type": "offer", "offer_code": "QOWGX", "offer_url": "http://hp.com/?offercode=QOWGX", "offer_description": "pre-launch offer", "openDay":"2016-04-29T18:37:21.766000", "closeDay": "2016-04-29T18:37:21.766000"}], "socialex":[{"socialmedia_type":"facebook", "socialmedia_url":"http://facebook.com/series-5.com", "socialmedia_headline": "facebook free basic campaign"}, {"socialmedia_type":"twitter", "socialmedia_url":"http://twitter.com/series-5.com", "socialmedia_headline": "twitter free basic campaign"}]}' http://localhost:8000/mediacontent/ads/imageads/571a72741d41c8b297ff2e75/

# Add Image to an ImageAd
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" http://127.0.0.1:8000/mediacontent/ads/imageads/571a72741d41c8b297ff2e75/572704641d41c8e673f4848d/

# Do a research
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "helmet", "query_type": "multifield", "query_object_type": "Campaign", "query_fields":{"category":4, "description":2}}' http://127.0.0.1:8000/research/search/

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "hel.*", "query_type": "regexp", "query_object_type": "Campaign", "query_fields":{"category":4}}' http://127.0.0.1:8000/research/search/

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "helmet"}' http://127.0.0.1:8000/research/search/

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "Inorbit", "query_type": "multifield", "query_object_type": "MediaAggregate"}' http://127.0.0.1:8000/research/search/mediaaggregate/

curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"raw_strings": "Bangalore", "query_type": "multifield", "query_object_type": "OOHMediaSource", "query_fields":{"city":4, "name":2}}' http://172.31.41.248:8000/research/search/

# Term query for MediaAggregate
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"query":{"termquery": [{"name": "Inorbit"},{"city": "Bangalore"}],"optype": "And"},"query_type": "structured", "query_object_type": "MediaAggregateLocation"}' http://127.0.0.1:8000/research/search/_sql/

# Location sensed query for MediaAggregate
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"query": {"geodistancefilter": {"field": "location","fieldvalue": [12.975667, 77.729083],"distance": 0.01},"optype": "And"},"query_type": "structured", "query_object_type": "MediaAggregateLocation"}' http://127.0.0.1:8000/research/search/_sql/

# Location sensed query for Campaign in Mediaaggregate
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"query": {"geodistancefilter": {"field": "location","fieldvalue": [12.975667, 77.729083],"distance": 0.01},"optype": "And"},"query_type": "structured", "query_object_type": "CampaignByMaLocation"}' http://127.0.0.1:8000/research/search/_sql/

# Location sensed query for Campaign in OOH
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"query": {"geodistancefilter": {"field": "point","fieldvalue": [12.975667, 77.729083],"distance": 50},"optype": "And"},"query_type": "structured", "query_object_type": "CampaignByMediaSourceLocation"}' http://127.0.0.1:8000/research/search/_sql/

# Invoking search API internally, doesn't do any user validations.
curl -H "Content-Type: application/json" -X POST -d '{"raw_strings": "fitness", "query_type": "OOHMediaSource", "query_fields":{"category":4, "description":2}}' http://127.0.0.1:8000/research/query/

# Submitting OOH operational data for analytics (Bulk upload)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '[{"visitor_total_count":170000, "breakups": {"age":{"15-20": 100, "20-28": 200, "28-35": 500}, "commute":{"bus":500,"cabs": 1200,"cars": 1500}, "target":{"profs":1200, "teens":5000, "biz":5000}}, "feed_timestamp":"2016-06-01T18:37:21.766000"}, {"visitor_total_count":3500, "breakups": {"age":{"15-20": 100, "20-28": 200, "28-35": 500}, "commute":{"bus":500,"cabs": 1200,"cars": 1500}, "target":{"profs":1200, "teens":5000, "biz":5000}}, "feed_timestamp":"2016-06-02T18:37:21.766000"}]' http://127.0.0.1:8000/etl/ooh/574d68571d41c8ba3f289e84/

# Submitting OOH operational data for analytics (One sample)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '[{"visitor_total_count":170000, "breakups": {"age":{"15-20": 100, "20-28": 200, "28-35": 500}, "commute":{"bus":500,"cabs": 1200,"cars": 1500}, "target":{"profs":1200, "teens":5000, "biz":5000}}, "feed_timestamp":"2016-06-01T18:37:21.766000"}]' http://127.0.0.1:8000/etl/ooh/574d68571d41c8ba3f289e84/

# Retrieving OOH operational data (Many samples)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/etl/ooh/574d68571d41c8ba3f289e84/?startday=2016-06-02&endday=2016-08-02

# Retrieving OOH operational data (Many samples)
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/etl/ooh/574d68571d41c8ba3f289e84/

### Modeller ads

# OOH planner
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"wish": "credit loan ad", "filters": [{"type": "costfilter", "condition": "maximum", "value": "100000"}, {"type": "dgfilter", "condition": "target", "value": "parents"}]}' http://127.0.0.1:8000/modeller/planner/ooh/

### Planner Cloud Notifications

# send to only Male users
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"topic": "Account Balance Low","type": "notification", "message": "Some useful message to the consumer", "selector" : {"raw_strings": "male", "query_type": "multifield", "query_fields":{"gender":4}}}' http://127.0.0.1:8000/modeller/planner/notification/

# Send to all Users in the system from city=Delhi
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"topic": "Forum Mall Sale","type": "data", "content": {"context": "campaign", "content_ref": ["id1","id2"]}, "selector" : {"raw_strings": "Delhi", "query_type": "multifield", "query_fields":{"city":4}}}' http://127.0.0.1:8000/modeller/planner/notification/

# Send to all Users in the system.
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"topic": "Forum Mall Sale","type": "data", "content": {"context": "campaign", "content_ref": ["id1","id2"]}, "selector" : {}}' http://127.0.0.1:8000/modeller/planner/notification/


### Online media source
# Create online source
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "superbeing-test", "type" : "online", "display_name": "superbeing-test", "caption": "Wellness", "tags": "wellness", "home_url":"http://superbeing.in", "verification_url":"http://superbeing.in",  "category": "wellness", "fence": [12.99, 77.89], "radius": 100 }' http://127.0.0.1:8000/mediacontent/mediasource/online/

# Query campaigns running in the cloud source.
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/playing/cloudmediasource/?"id=590593e51d41c8402383a716"

### Physical web objects
# creating venue
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"venue_name": "somename", "venue_address": "someaddr", "venue_meta": {}}' http://127.0.0.1:8000/mediacontent/mediasource/venue/

# attach an existing sensor to venue
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"sensor_data": {"name":"simplename", "display_name":"simplename", "caption":"simplename", "uuid": "06091979", "type": "beacon", "range": "10", "location": [19.0, 20.0], "name":"gp11", "major":"2", "minor":"3", "beacon_type":"ibeacon", "max_tx_power":"63", "broadcast_url":"http://series-5.com"},"sensor_type": "Beacon"}' http://127.0.0.1:8000/mediacontent/mediasource/venue/592ef0db1d41c879e15a5ad4/?action=attach

# attach a venue to the OOHMediaSource
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediasource/ooh/57d844351d41c87ef6affad9/?action=addvenue&id=592ec9ca1d41c87120963ed2"

# attach a venue to the MediaAggregate
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediaaggregates/57d844351d41c87ef6affad9/?action=addvenue&id=592ec9ca1d41c87120963ed2"

# attach a campaign to the venue
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"start_date" : "2016-02-25T18:37:21.766000","end_date" :"2016-02-25T18:37:21.766000"}' "http://127.0.0.1:8000/mediacontent/mediasource/venue/592ec9ca1d41c87120963ed2/?action=addcontent&id=57c062231d41c83e549e8af9"

# API to query playing campaign on a venue
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/playing/venue/?"id=5931a53a1d41c81914155a2a"

# API to query venue activity
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediasource/venue/593d6b4f1d41c8c9cdd1b10b/activity/

# API to get sensor activity
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediasource/sensor/$id/activity/

# API to post a sensor activity (user checkin, checkout, disable)
# Choose "activity_type" in range {check-in = 1, check-out = 2, opt-out = 3}
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"activity_type": 1, "activity_data": {} }' "http://127.0.0.1:8000/mediacontent/mediasource/sensor/$id/activity/"

# Get a venue
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/mediasource/venue/$id/

# Get venue applicable to a MediaAggregate
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET "http://127.0.0.1:8000/mediacontent/mediasource/venue/?action=filter_by_mediaagregate&id=57d844351d41c87ef6affad9/"

### Tools
# Tool for creating campaign
python ./campaign_import.py tabseparated_camp.data http://127.0.0.1:8000 /home/sonu/adimages/campaigns/
# Tool for importing Ads to a campaign
python ./ad_import.py tabseparated_ad.data http://127.0.0.1:8000 /home/sonu/adimages/campaigns/ 570746dd1d41c84bc448786b


### Wishlists


# add venue to the mall, ooh etc.

# Attach a content to venue (plays the content when a sensor is detected)




# API to attach a campaign to a OOHMediaSource
POST http://localhost:8000/mediacontent/oohmediasource/<$source_id>/?action=addcontent&id=<$id> -d {}
 - Create a playing relation for each $source_id and $contentid field
 - playing field should be bound by "start date", "end date" and "enabled"

# API to query campaigns attached to a OOHMediaSource
GET http://localhost:8000/mediacontent/playing/oohmediasource/?id=<$sourceid> -d '{}'
 - Returns Playing objects
 - Each playing object represents the Campaign
 - For each Campaign (Id), list all the Ads under a campaign

# API to get all sources where the campaign is playing
GET http://localhost:8000/mediacontent/playing/campaign/?id=<$campaign-id> -d '{}'
 - Returns source instances

# __END__

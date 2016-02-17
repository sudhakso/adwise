# README #

This README documents the steps that are necessary to get your AdWise application up and running.

### What is this repository for? ###

* Quick summary
AdWise system comprises of User management application, Mediacontent management application and Advertisement analytics related applications.
In future other relevant application will be added.

* Version
0.1 master


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
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "user": {"username": "serviceuser@series-5.com","password":"adwise123","address": "TBD","city":"Bangalore","state":"Karnataka","point": [0.0, 0.0], "phone_number":"9880563410", "email":"serviceuser@series-5.com", "gender": "Male", "pin": "560048"}}' http://localhost:8000/users/

# Create a demo User
sudo curl -H "Content-Type: application/json" -H "username:demouser@series-5.com" -H "password:demo123" -H "email:demouser@series-5.com" -X POST -d '{ "user": {"username": "demouser@series-5.com","password":"demo123","address": "TBD","city":"Bangalore","state":"Karnataka","point": [0.0, 0.0], "phone_number":"9880563410", "email":"demouser@series-5.com", "gender": "Male", "pin": "560048"}}' http://localhost:8000/users/

# Create agency/project and a user together
 sudo curl -H "Content-Type: application/json" -H "username:lion4" -H "password:lion1234" -H "email:lion4@jungle.com" -X POST -d '{ "user": {"username": "lion4","password":"lion1234","address": "742 Evergreen Terrace","city":"Springfield","state":"Oregon","point": [-123.0208, 44.0464], "phone_number":"roar", "email":"lion4@jungle.com", "gender": "Male", "pin": "560077"}, "project": {"name": "somename", "type": "Media Agency", "address": "somelocation", "city": "Bangalore", "state": "Karnataka", "pin":"560077"}, "role" : {"name":"r1"}}' http://localhost:8000/users/

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
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{ "name" : "kundanahalli_40x40", "type" : "ooh", "street_name" : "kundanahalli railway gate", "city" : "Bangalore", "state" : "Karnataka", "country" : "India", "point": [124.78, 32.0], "size": [10, 4], "pin" : "560057", "pricing" : { "name" : "diwali", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000"}, "booking" : { "start_time" : "2016-02-25T18:37:21.766000", "duration" : 10, "type" : "educational"}}' http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Update image for OOH
curl -X POST -S -H 'Accept: application/json' -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" http://127.0.0.1:8000/mediacontent/mediasource/ooh/56b5f4ca1d41c85e256e11c2/

# Storing a share/like/dislike request by Billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST  -d '{"activity_meta" : "email=sonu@g.com, phone=ksksk"}' http://localhost:8000/mediacontent/mediasource/activity/share/56c0b94c1d41c8957cba8237

# Fetching a share/like/dislike activity by billboard
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/mediasource/activity/share/56c0b94c1d41c8957cba8237


# Miscellaneous
# Create a service called 'location' for the User
sudo curl -H "Content-Type: application/json" -X POST -d '{"target_service_name": "location", "service_meta": "empty"}' http://localhost:8000/users/services/lion2/location/

# Create an ImageAd for a campaign
curl -X POST -S -H 'Accept: application/json' -F "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg" -F "display_url"="http://hp.com" -F "final_urls"="http://hp.com" -F "mobile_urls"="http://hp.com" -F "app_urls"="http://hp.com" -F "thirdparty_tracking_url"="http://track.com" -F "adwise_tracking_url"="http://hp.com" -F "ad_type"="ImageAd" http://127.0.0.1:8000/mediacontent/ads/imageads/5677bbb31d41c84312e9cd91/

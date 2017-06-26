# README #

This README documents the concepts and API to interact with Physical Web objects.

* Quick summary

Sensors form the most basic element in the workd of PhysicalWeb. And using AdWise, user's can attach a pre-defined content to such Sensors.
Adwise platform hosts these content and relays them to user's mobile application based on "Device enter" event received through the AdWise SDK.

For more information on the data model, please see "physicalweb-model.md".
In our model, each Venue constitues a bunch of different types of sensors. And in a typical Shopping Mall deployments, the retail shops could have 1 or more such Venues.
Venue defines the logical unit where the Retail shop owners could configure the personalization related aspects for the sensed content (for example, what is the target group, geneder etc.)

Each sensor is identified with its unique ID. for example, in case of iBeacon this is the Beacon UUID. When the research app or the SDK senses the physical beacon in on-premise installation in the Retail shop or Mall, it sends the beacon UUID to the AdWise backend.
AdWise backend returns the attached content to the SDK/research app.

* Version
0.1.01 master

# creating venue
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"venue_name": "somename", "venue_address": "someaddr", "venue_meta": {}}' http://127.0.0.1:8000/mediacontent/mediasource/venue/

# attach a sensor to venue
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"sensor_data": {"name":"simplename", "display_name":"simplename", "caption":"simplename", "uuid": "8e0e714daf3b3e00336a", "type": "beacon", "range": "10", "location": [19.0, 20.0], "name":"gp11", "major":"2", "minor":"3", "beacon_type":"ibeacon", "max_tx_power":"63", "broadcast_url":"http://series-5.com"},"sensor_type": "Beacon"}' http://127.0.0.1:8000/mediacontent/mediasource/venue/592ef0db1d41c879e15a5ad4/?action=attach

# attach a venue to the OOHMediaSource
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediasource/ooh/57d844351d41c87ef6affad9/?action=addvenue&id=592ec9ca1d41c87120963ed2"

# attach a venue to the MediaAggregate
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{}' "http://127.0.0.1:8000/mediacontent/mediaaggregates/57d844351d41c87ef6affad9/?action=addvenue&id=592ec9ca1d41c87120963ed2"

# attach a campaign to the venue
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"start_date" : "2016-02-25T18:37:21.766000","end_date" :"2016-02-25T18:37:21.766000"}' "http://127.0.0.1:8000/mediacontent/mediasource/venue/592ec9ca1d41c87120963ed2/?action=addcontent&id=57c062231d41c83e549e8af9"

# API to query playing campaign on a venue
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/playing/venue/?"id=5931a53a1d41c81914155a2a"

# API to query playing campaign on a sensor
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://127.0.0.1:8000/mediacontent/playing/sensor/?"id=06091980"

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
 curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET "http://ec2-35-167-104-107.us-west-2.compute.amazonaws.com:8000/mediacontent/mediasource/venue/?action=filter_by_mediaaggregate&id=59343622981c926d5a284c61"

# Campaign Management
# update short url for the campaign as part of CampaignTracking objects
sudo curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X POST -d '{"name": "gp-2", "description": "gp flipkart offers", "language_code": "en"}' http://localhost:8000/mediacontent/campaign/59511ec71d41c8f7e82c0daf/track/

#retrieve the short URL for the campaign to program into sensor
curl -H "Content-Type: application/json" -H "username:serviceuser@series-5.com" -H "password:adwise123" -H "email:serviceuser@series-5.com" -X GET http://localhost:8000/mediacontent/campaign/59511ec71d41c8f7e82c0daf/track/

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

Django==1.6.11
Pillow==3.0.0
PyYAML==3.11
amqp==1.4.8
anyjson==0.3.3
argparse==1.2.1
billiard==3.3.0.22
blinker==1.4
celery==3.1.19
django-mongodb-engine==0.6.0
django-rest-framework-mongoengine==2.0.2
django-rest-swagger==0.3.4
djangorestframework==3.2.4
djangotoolbox==1.8.0
kombu==3.0.32
mongoengine==0.10.0
pymongo==3.0.3
pytz==2015.7
wsgiref==0.1.2

OS System components are 
(1) MONGODB  
(2) sudo apt-get install libjpeg8-dev
(3) sudo apt-get install rabbitmq-server
* Database configuration
This project uses MONGODB.

* How to run tests
python manage.py tests

* Deployment instructions
(1) Create a Virtual environment project.
(2) Activate the environment by running, <projectfolder>/bin/activate.
    It should give you a prompt like 
   (project_name)user@ubuntu:>
(3) git clone git@bitbucket.org:adwise-m/adwise-userprofile-mgr.git
(4) pip install -r requirements.txt
(5) Install MONGODB using sudo apt-get, get the latest.
(6) Perform, sudo apt-get install libjpeg8-dev
(7) Perform, sudo apt-get install rabbitmq-server
(8) Start the AdWise server using the command,
    (project_name)user@ubuntu:> python manage.py runserver.
(9) To verify everything is fine open Browser,
    http://127.0.0.1:8000/ 
    should display the swagger API page.
    

### Contribution guidelines ###
To be drafted.

### Who do I talk to? ###

series-5
'''
Created on Feb 7, 2016

@author: sonu
'''
import os
import sys
from datetime import datetime, timedelta
import json
import requests
import re
from userapp.models import MediaUser

# Basic authentication
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


# Re-creates dJango AUTH users from MediaUser entries.
# dJango Auth model differs in implementation by Mongo DB version
# and may not be directly portable.

if __name__ == '__main__':
    all_users = MediaUser.objects.all()
    print "Found %d users..." % len(all_users)
    for user in all_users:
        print 'Loading user [%s]' % user.username
        try:
            user = User.objects.get(username=user.username)
            if user:
                print 'User already exists, skipping...'
                continue
        except ObjectDoesNotExist:
            print "Creating user with username: %s, email: %s, passowrd: %s" % (user.username, user.email, user.password)
            # User doesn't exist.
#             usr = User.objects.create(username=user.username,
#                                       email=user.email)
#             usr.set_password(usr.password)
#             usr.save()
            print 'Finished adding user %s...' % user.username


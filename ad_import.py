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


def main(sourcefile):
    d = []
    dhead = []
    firstline = True
    with open(sourcefile, 'rb') as source:
        for line in source:
            fields = line.split('\t')
            if firstline:
                dhead = fields
                firstline = False
            else:
                d.append(fields)
    return dhead, d


def load_ad(fields, ignore_fields, row):
    # an instance
    ad = {}
    offer = {}
    misc = {}
    index = 0
    for field in fields:
        if field not in ignore_fields:
            field = field.strip().rstrip('\n')
            val = float(row[index]) if row[index].isdigit() else row[index].strip()
            # check for extensions in the header
            if ':' in field:
                toks = field.split(':')
                offer[toks[1]] = val
            # Check the value, if it is a list
            elif field == 'ad_location_tag':
                # Value is a list
                m = re.match(r'\"\[(\d+.\d+),(\d+.\d+)\]*\"', val)
                if m:
                    val = [float(i) for i in m.groups(0)]
                ad[field] = val
            else:
                ad[field] = val
        else:
            misc[field] = row[index]
        index = index + 1
    if offer:
        ad['offerex'] = [offer]
    return (misc, ad)


def process_ad(ad):
    image = {}

    if 'image' in ad:
        # process image
        # "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"
        if ad['image'] == '':
            ad.pop('image', None)
        else:
            image_value = ad['image']
            ad['image'] = image_value

    return ad


def post_ad(url, auth_dict, ad, imagedir=None):
    headers = {'Content-Type': 'application/json',
               "username": auth_dict['username'],
               "password": auth_dict['password'],
               "email": auth_dict['email']
               }
    image_headers = {"username": auth_dict['username'],
                     "password": auth_dict['password'],
                     "email": auth_dict['email']}
    image_filename = auth_dict['image'] if 'image' in auth_dict else ''

    payload = ad
    json_camp = json.loads(ad)
    req = requests.Request('POST', url, data=payload, headers=headers)
    prep_req = req.prepare()
    pretty_print_POST(prep_req)
    s = requests.Session()
    r = s.send(prep_req)
    json_content = json.loads(r.content)
    if image_filename and 'id' in json_content:
        print 'Trying to load the image %s' % image_filename
        # Update the campaign with the image
        url = "%s%s/" % (url, json_content['id'])
        if imagedir is None:
            image_file = '%s/%s' % (
                            os.path.dirname(os.path.abspath(__file__)),
                            image_filename)
        else:
            image_file = '%s/%s' % (
                            imagedir,
                            image_filename)
        files = {'image': open(image_file, 'rb'),
                 'Content-Type': 'image/jpeg'}
        requests.post(url, headers=image_headers, files=files)

# Invoke it with, agrv[1]=> data, argv[2] => http://127.0.0.1:8000
# argv[3] => image-dir, argv[4] => campaign-id
# Keep the data in the same location where this script resides.
# Basically take the script to location where all files are present
# and run.
# Example, 
#/home/sonu/thomas/atlas/upstream/up/bin/python ad_import.py
# tabseparated_ad.data 
# http://ec2-52-10-208-37.us-west-2.compute.amazonaws.com:8000/ 
# /home/sonu/adimages/campaigns 
# 571b8a87c0c95445f8cb396e

if __name__ == '__main__':
    (columns, data) = main(sys.argv[1])
    ignore_fields = ['email', 'username', 'password', 'image', 'dummy']
    for eachrow in data:
        misc, ad = load_ad(columns, ignore_fields, eachrow)
        processed_ad = process_ad(ad)
        json_processed_ad = json.dumps(processed_ad)
        post_ad(("%s/%s/%s/" % (sys.argv[2],
                                'mediacontent/ads/imageads',
                                sys.argv[4])),
                misc, json_processed_ad, imagedir=sys.argv[3])


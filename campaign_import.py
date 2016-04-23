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


def load_campaign(fields, ignore_fields, row):
    # an instance
    camp = {}
    misc = {}
    index = 0
    city = []
    state = []
    country = []
    for field in fields:
        if field not in ignore_fields:
            field = field.strip().rstrip('\n')
            val = float(row[index]) if row[index].isdigit() else row[index].strip()
            if field == 'city':
                city.append(val.strip(','))
            elif field == 'state':
                state.append(val.strip(','))
            elif field == 'country':
                country.append(val.strip(','))
            else:
                # Check the value, if it is a list
                if field == 'geo_tags':
                    # Value is a list
                    m = re.match(r'\"\[(\d+.\d+),(\d+.\d+)\]*\"', val)
                    if m:
                        val = [float(i) for i in m.groups(0)]
                camp[field] = val
        else:
            misc[field] = row[index]
        index = index + 1
    camp['city'] = city
    camp['state'] = state
    camp['country'] = country
    return (misc, camp)


def process_campaign(camp):
    image = {}

    if 'image' in camp:
        # process image
        # "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"
        if camp['image'] == '':
            camp.pop('image', None)
        else:
            image_value = camp['image']
            camp['image'] = image_value

    return camp


def post_campaign(url, auth_dict, camp, imagedir=None):
    headers = {'Content-Type': 'application/json',
               "username": auth_dict['username'],
               "password": auth_dict['password'],
               "email": auth_dict['email']
               }
    image_headers = {"username": auth_dict['username'],
                     "password": auth_dict['password'],
                     "email": auth_dict['email']}

    payload = camp
    json_camp = json.loads(camp)
    req = requests.Request('POST', url, data=payload, headers=headers)
    prep_req = req.prepare()
    pretty_print_POST(prep_req)
    s = requests.Session()
    r = s.send(prep_req)
    json_content = json.loads(r.content)
    if 'id' in json_content:
        # Update the campaign with the image
        url = "%s%s/" % (url, json_content['id'])
        if imagedir is None:
            image_file = '%s/%s' % (
                            os.path.dirname(os.path.abspath(__file__)),
                            json_camp['image'])
        else:
            image_file = '%s/%s' % (
                            imagedir,
                            json_camp['image'])
        files = {'image': open(image_file, 'rb'),
                 'Content-Type': 'image/jpeg'}
        requests.post(url, headers=image_headers, files=files)

# Invoke it with, agrv[1]=> data, argv[2] => http://127.0.0.1:8000
# Keep the data in the same location where this script resides.
# Basically take the script to location where all files are present
# and run.

if __name__ == '__main__':
    (columns, data) = main(sys.argv[1])
    ignore_fields = ['email', 'username', 'password', 'dummy']
    for eachrow in data:
        misc, camp = load_campaign(columns, ignore_fields, eachrow)
        processed_campaign = process_campaign(camp)
        json_processed_campaign = json.dumps(processed_campaign)
        post_campaign(("%s/%s" % (sys.argv[2], 'mediacontent/campaign/')),
                      misc, json_processed_campaign, imagedir=sys.argv[3])


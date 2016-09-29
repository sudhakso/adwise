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


def load_mas(fields, ignore_fields, row):
    # an instance
    ma = {}
    misc = {}
    index = 0
    for field in fields:
        dict_data = {}
        if field not in ignore_fields:
            field = field.strip().rstrip('\n')
            val = float(row[index]) if row[index].isdigit() else row[index].strip()
            # Check the value, if it is a list
            if field == 'location':
                # Value is a list
                m = re.match(r'\"\[(\d+.\d+),(\d+.\d+)\]*\"', val)
                if m:
                    val = [float(i) for i in m.groups(0)]
            if field == 'internet_settings' or field == 'poi_marker_data':
                # {home_url: http://inorbit.in/whitefield/}
                m = re.match(r'\{([A-Za-z_]+):([A-Za-z_/.:0-9]+)\}*', val)
                if m:
                    dict_data[m.groups(0)[0]] = m.groups(0)[1]
                    val = dict_data
            ma[field] = val
        else:
            misc[field] = row[index]
        index = index + 1
    return (misc, ma)


def process_mas(ma):
    image = {}
    if 'image' in ma:
        # process image
        # "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"
        if ma['image'] == '':
            ma.pop('image', None)
        else:
            image_value = ma['image']
            ma['image'] = image_value

    return ma


def post_ma(url, auth_dict, ma):
    headers = {'Content-Type': 'application/json',
               "username": auth_dict['username'],
               "password": auth_dict['password'],
               "email": auth_dict['email']
               }
    image_headers = {"username": auth_dict['username'],
                     "password": auth_dict['password'],
                     "email": auth_dict['email']}

    payload = ma
    json_ma = json.loads(ma)
    req = requests.Request('POST', url, data=payload, headers=headers)
    prep_req = req.prepare()
    pretty_print_POST(prep_req)
    s = requests.Session()
    r = s.send(prep_req)
    json_content = json.loads(r.content)
    if 'id' in json_content:
        # Update the OOH with the image
        url = "%s%s/" % (url, json_content['id'])
        image_file = '%s/%s' % (
                        os.path.dirname(os.path.abspath(__file__)),
                        json_ma['image'])
        files = {'image': open(image_file, 'rb'),
                 'Content-Type': 'image/jpeg'}
        requests.post(url, headers=image_headers, files=files)

# Invoke it with, agrv[1]=> data, argv[2] => http://127.0.0.1:8000
# Keep the data in the same location where this script resides.
# Basically take the script to location where all files are present
# and run.

if __name__ == '__main__':
    (columns, data) = main(sys.argv[1])
    ignore_fields = ['email', 'username', 'password']
    for eachrow in data:
        misc, mas = load_mas(columns, ignore_fields, eachrow)
        processed_mas = process_mas(mas)
        json_processed_mas = json.dumps(processed_mas)
        post_ma(("%s/%s" % (sys.argv[2], 'mediacontent/mediaaggregates/')),
                misc, json_processed_mas)


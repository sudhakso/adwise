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
            val = float(row[index]) if row[index].isdigit() else row[index].strip()
            if field == 'campaign':
                # [CapitalOne,somethingelse]
                print val
                m = re.match(r'\"\[([A-Za-z_,0-9 ]+)\]*\"', val)
                if m:
                    cns = m.groups(0)[0]
                    val = cns.split(',')
            # set the val
            misc[field] = val
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


def _process_campaigns_for_aggregate(base_url, head, ma_id, camp_names):
    # url=/research/search/
    camp_ids = []
    if camp_names:
        headers = {'Content-Type': 'application/json',
                   "username": head['username'],
                   "password": head['password'],
                   "email": head['email']
                   }
    # Fetch all campaigns
    namedict = {"name": '5'}
    _url = ("%s/%s" % (base_url, 'research/search/'))
    for name in camp_names:
        payload = {"raw_strings": name,
                   "query_type": "multifield",
                   "query_object_type": "Campaign",
                   "query_fields": namedict}
        jsonpayload = json.dumps(payload)
        req = requests.Request('POST', _url, data=jsonpayload, headers=headers)
        prep_req = req.prepare()
        pretty_print_POST(prep_req)
        s = requests.Session()
        r = s.send(prep_req)
        json_content = json.loads(r.content)
        if 'campaigns' in json_content:
            camps = json_content['campaigns']
            for acamp in camps:
                if 'id' in acamp:
                    print 'Adding campaign %s' % acamp['id']
                    camp_ids.append(acamp['id'])
    # Attach Campaigns to MA
    # data = '{"start_date" : "2016-02-25T18:37:21.766000","end_date" :"2016-02-25T18:37:21.766000"}'
    # url = "http://127.0.0.1:8000/mediacontent/mediaaggregates/57d844351d41c87ef6affad9/?action=addcontent&id=57c062201d41c83e549e8ae5"
    if camp_ids:
        payload = {
                   "start_date": str(datetime.now()),
                   "end_date": str(datetime.now() + timedelta(days=300))
                   }
        jsonpayload = json.dumps(payload)
        for camp_id in camp_ids:
            _url = ("%s/%s%s/?action=addcontent&id=%s" % (
                                            base_url,
                                            'mediacontent/mediaaggregates/',
                                            ma_id,
                                            camp_id))
            req = requests.Request('POST', _url, data=jsonpayload,
                                   headers=headers)
            prep_req = req.prepare()
            pretty_print_POST(prep_req)
            s = requests.Session()
            r = s.send(prep_req)
            json_content = json.loads(r.content)


def post_ma(base_url, auth_dict, ma, imagedir):
    headers = {'Content-Type': 'application/json',
               "username": auth_dict['username'],
               "password": auth_dict['password'],
               "email": auth_dict['email']
               }
    image_headers = {"username": auth_dict['username'],
                     "password": auth_dict['password'],
                     "email": auth_dict['email']}
    _url = ("%s/%s" % (base_url, 'mediacontent/mediaaggregates/'))
    payload = ma
    req = requests.Request('POST', _url, data=payload, headers=headers)
    prep_req = req.prepare()
    pretty_print_POST(prep_req)
    s = requests.Session()
    r = s.send(prep_req)
    json_content = json.loads(r.content)
    if 'id' in json_content:
        # Update the OOH with the image
        _url = "%s%s/" % (_url, json_content['id'])
        if imagedir is None:
            image_file = '%s/%s' % (
                            os.path.dirname(os.path.abspath(__file__)),
                            auth_dict['image'])
        else:
            image_file = '%s/%s' % (
                            imagedir,
                            auth_dict['image'])
        files = {'image': open(image_file, 'rb'),
                 'Content-Type': 'image/jpeg'}
        requests.post(_url, headers=image_headers, files=files)
        # Set the campaigns.
        if 'campaign' in auth_dict:
            print 'Setting campaigns %s for aggregate %s' % (
                                                auth_dict['campaign'],
                                                json_content['id'])
            _process_campaigns_for_aggregate(base_url, headers,
                                             json_content['id'],
                                             auth_dict['campaign'])

# Invoke it with, agrv[1]=> data, argv[2] => http://127.0.0.1:8000
# Keep the data in the same location where this script resides.
# Basically take the script to location where all files are present
# and run.

if __name__ == '__main__':
    (columns, data) = main(sys.argv[1])
    ignore_fields = ['email', 'username', 'password', 'image', 'campaign', 'dummy']
    for eachrow in data:
        misc, mas = load_mas(columns, ignore_fields, eachrow)
        processed_mas = process_mas(mas)
        json_processed_mas = json.dumps(processed_mas)
        post_ma(sys.argv[2],
                misc, json_processed_mas,
                imagedir=sys.argv[3] if len(sys.argv) >= 4 else None)


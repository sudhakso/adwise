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


def load_ooh(fields, ignore_fields, row):
    # an instance
    ooh = {}
    misc = {}
    index = 0
    list_data = []
    for field in fields:
        if field not in ignore_fields:
            field = field.strip().rstrip('\n')
            val = float(row[index]) if row[index].isdigit() else row[index].strip()
            if field == 'sizeW':
                list_data.append(val)
            elif field == 'sizeH':
                list_data.append(val)
            else:
                # Check the value, if it is a list
                if field == 'point':
                    # Value is a list
                    m = re.match(r'\"\[(\d+.\d+),(\d+.\d+)\]*\"', val)
                    if m:
                        val = [float(i) for i in m.groups(0)]
                ooh[field] = val
        else:
            misc[field] = row[index]
        index = index + 1
    ooh['size'] = list_data
    return (misc, ooh)


def process_ooh(ooh):
    booking = {}
    pricing = {}
    image = {}

    if 'booking' in ooh:
        # process booking
        if ooh['booking'].upper() == 'IMMEDIATELY':
            ooh.pop('booking', None)
        else:
            # "start_time" : "2016-02-25T18:37:21.766000",
            # "duration" : 10,
            # "type" : "educational"
            st = datetime.now().date()
            et = datetime.strptime(ooh['booking'], '%d.%m.%Y').date()
            booking['duration'] = abs((et - st).days)
            booking['start_time'] = str(datetime.now())
            booking['end_time'] = str(datetime.now() + timedelta(
                                                        days=booking['duration']))
            booking['type'] = 'Unknown'

            ooh['booking'] = booking
    if 'pricing' in ooh:
        # process pricing
        # "name" : "diwali", "currency" : "INR", "unit" : "perSq.Ft.", "rate" : 5, 
        # "offer_start_time" : "2016-02-25T18:37:21.766000", "offer_end_time" : "2016-02-25T18:37:21.766000",
        # "price" : 2130
        if ooh['pricing'] == '':
            ooh.pop('pricing', None)
        else:
            pricing['name'] = 'Not Mentioned'
            pricing['currency'] = 'INR'
            pricing['unit'] = 'perSq. Ft.'
            pricing['rate'] = ooh['pricing']
            pricing['offer_start_time'] = datetime.now()
            pricing['offer_end_time'] = datetime.now()

            ooh['pricing'] = pricing
    if 'image' in ooh:
        # process image
        # "image=@/home/sonu/adimages/chineese_ad.jpg;type=image/jpg"
        if ooh['image'] == '':
            ooh.pop('image', None)
        else:
            image_value = ooh['image']
            ooh['image'] = image_value

    return ooh


def post_ooh(url, auth_dict, ooh):
    headers = {'Content-Type': 'application/json',
               "username": auth_dict['username'],
               "password": auth_dict['password'],
               "email": auth_dict['email']
               }
    image_headers = {"username": auth_dict['username'],
                     "password": auth_dict['password'],
                     "email": auth_dict['email']}

    payload = ooh
    json_ooh = json.loads(ooh)
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
                        json_ooh['image'])
        files = {'image': open(image_file, 'rb'),
                 'Content-Type': 'image/jpeg'}
        requests.post(url, headers=image_headers, files=files)

# Invoke it with, agrv[1]=> data, argv[2] => http://127.0.0.1:8000
# Keep the data in the same location where this script resides.
# Basically take the script to location where all files are present
# and run.

if __name__ == '__main__':
    (columns, data) = main(sys.argv[1])
    ignore_fields = ['Company', 'email', 'username', 'password']
    for eachrow in data:
        misc, ooh = load_ooh(columns, ignore_fields, eachrow)
        processed_ooh = process_ooh(ooh)
        json_processed_ooh = json.dumps(processed_ooh)
        post_ooh(("%s/%s" % (sys.argv[2], 'mediacontent/mediasource/ooh/')),
                 misc, json_processed_ooh)


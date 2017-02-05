'''
Created on Aug 19, 2016

@author: sonu
'''

from jinja2 import Template
import json
from django.conf import settings


class CloudNotifierMessageTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MODELLER_DIR,
                                           'templates/cloudnotifier_message.j2'),
                                 'r').read())

    def create_message(self, **kwargs):
        # Create the serializer
        rendered = str(self.j2_template.render(**kwargs))
        rendered = rendered.replace("\'","\"").replace("u\"","\"").replace("u\'","\'")
        return rendered

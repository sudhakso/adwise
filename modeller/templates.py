# -*- coding: utf-8 -*-

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
        rendered = self.j2_template.render(**kwargs).encode('utf-8')
#         rendered = rendered.replace("\'","\"").replace("u\"","\"").replace("u\'","\'")
        rendered = rendered.replace("\'","\"")
        return rendered


class CloudNotifierDataMessageTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MODELLER_DIR,
                                           'templates/clouddata_message.j2'),
                                 'r').read())

    def create_message(self, **kwargs):
        # Create the serializer
        rendered = self.j2_template.render(**kwargs).encode('utf-8')
        rendered = rendered.replace("\'","\"")
        return rendered

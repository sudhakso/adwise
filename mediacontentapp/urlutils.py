'''
Created on Jun 26, 2017

@author: sonu
'''

import tinyurl


class URLDriver(object):

    def get_URL(self, url):
        return None


class TinyUrlDriver(URLDriver):
    '''
    classdocs
    '''

    def get_URL(self, url):
        return tinyurl.create_one(url)


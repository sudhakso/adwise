'''
Created on Jun 26, 2017

@author: sonu
'''

import tinyurl


class URLDriver(object):

    def get_URL(self, url, urlmeta=None):
        return None


class TinyUrlDriver(URLDriver):
    '''
    classdocs
    '''

    def get_URL(self, url, urlmeta=None):
        return tinyurl.create_one(url)


class Series5UrlDriver(URLDriver):
    '''
    classdocs
    '''

    def get_URL(self, url, urlmeta):
        # URL could be simply https://series-5.com/<campaign-id>

        # TBD (Note: Sonu) This should make an API call to series-5 URL hosting
        # service, and should not decide the URL format/content.
        # Workaround Fix: Forming campaign URL is temporary heer.
        BASE_URL = "https://series-5.com"
        campaignId = urlmeta['campaignId'] if 'campaignId' in urlmeta else None
        trackurl = "%s/%s" % (
                    BASE_URL, campaignId) if campaignId else "%s/" % (BASE_URL)
        return trackurl

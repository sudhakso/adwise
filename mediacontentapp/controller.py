'''
Created on Dec 12, 2015

@author: sonu
'''

# TODO(Sonu) : Controller to handle campaigns


class CampaignManager():

    def prepare_campaign(self, user_id, args):
        pass


class MediaSourceController():

    def process_query(self, *args):
        pass


class DashboardController():

    def update_dashboard(self, dash, args):
        pass

    def process_query(self, *args):
        pass


class ActivityManager():

    @staticmethod
    def get_activity_id(activity_name):
        activities = dict(share=1,
                          like=2,
                          dislike=3)

        if activity_name in activities:
            return activities[activity_name]
        else:
            return -1

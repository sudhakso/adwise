class ActivityManager():

    @staticmethod
    def get_activity_id(activity_name):
        activities = dict(share=1,
                          like=2,
                          dislike=3,
                          quote=4,
                          view=5)

        if activity_name in activities:
            return activities[activity_name]
        else:
            return -1

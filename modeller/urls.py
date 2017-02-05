from django.conf.urls import url, include
from modeller.views import TextClassifier,\
 Classifier
from modeller.plannerviews import OOHPlanner, NotifierView

# Wire up our API using automatic URL routing.
urlpatterns = [
     url(r'^classify/',
         TextClassifier.as_view()),
     url(r'^nbclassifier/load/',
         Classifier.as_view()),
     url(r'^planner/ooh/',
         OOHPlanner.as_view()),
     url(r'^planner/notification/',
         NotifierView.as_view()),
]

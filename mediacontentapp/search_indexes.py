from datetime import datetime
from haystack import indexes
from mediacontentapp.models import OOHMediaSource


class OOHMediaSourceIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Out of house advertising media type search index.
    """
  
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    display_name = indexes.CharField(model_attr='display_name')
    caption = indexes.CharField(model_attr='caption')
    
    street_name = indexes.CharField(model_attr='street_name')
    city = indexes.CharField(model_attr='city')
    state = indexes.CharField(model_attr='state')
    country = indexes.CharField(model_attr='country')
    pincode = indexes.CharField(model_attr='pin')
#     created_at = indexes.DateTimeField(model_attr='created_time')
 

    def get_model(self):
        return OOHMediaSource

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

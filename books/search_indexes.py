from haystack import indexes
from books.models import Bokks

class BokksIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True,use_teplate=True)
    
    def get_model(self):
        return Books
    def index_queryset(self,using=None):
        return self.get_model().objects.all()

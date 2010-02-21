from django.conf.urls.defaults import *
from errorbucket.buckets.handlers import BucketHandler

urlpatterns = patterns('',
  (r'(?P<key_name>[\w]+)$', BucketHandler()),
)

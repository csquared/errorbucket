from django.conf.urls.defaults import *
from errorbucket.buckets.handlers import BucketHandler

urlpatterns = patterns('errorbucket.buckets.views',
  (r'^$', UserBucketHandler()),
  (r'(?P<key_name>[\w]+)$', BucketHandler()),
)

from django.conf.urls.defaults import *
from errorbucket.buckets.handlers import UserBucketHandler, ErrorHandler

urlpatterns = patterns('',
  (r'^bucket$', UserBucketHandler()),
  (r'^errors$', ErrorHandler()),
  (r'(?P<key>[\w]+)$', ErrorHandler()),
  (r'^heroku', include('errorbucket.heroku.urls')),
  (r'^$', include('errorbucket.www.urls')),
)

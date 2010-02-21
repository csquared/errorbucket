from django.conf.urls.defaults import *
from errorbucket.buckets.handlers import UserBucketHandler

urlpatterns = patterns('',
  (r'^buckets', include('errorbucket.buckets.urls')),
  (r'^bucket$', UserBucketHandler()),
  (r'^heroku', include('errorbucket.heroku.urls')),
  (r'^$', include('errorbucket.www.urls')),
)

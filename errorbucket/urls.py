from django.conf.urls.defaults import *

urlpatterns = patterns('',
  (r'^buckets', include('errorbucket.buckets.urls')),
  (r'^bucket$', 'errorbucket.buckets.views.user_bucket'),
  (r'^heroku', include('errorbucket.heroku.urls')),
  (r'^$', include('errorbucket.www.urls')),
)

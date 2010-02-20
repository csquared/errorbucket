from django.conf.urls.defaults import *

urlpatterns = patterns('errorbucket.buckets.views',
  (r'^$', 'index'),
  (r'setup$', 'setup'),
)

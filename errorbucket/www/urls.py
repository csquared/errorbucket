from django.conf.urls.defaults import *

urlpatterns = patterns('errorbucket.www.views',
  (r'^$', 'index'),
)
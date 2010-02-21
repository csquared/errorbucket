#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'errorbucket.settings'

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import django.core.handlers.wsgi
  
def main():
  util.run_wsgi_app(django.core.handlers.wsgi.WSGIHandler())

if __name__ == '__main__':
  main()

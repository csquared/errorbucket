#!/usr/bin/env python
import logging, os, sys
from google.appengine.ext.webapp import util

# Remove the standard version of Django.
for k in [k for k in sys.modules if k.startswith('django')]:
    del sys.modules[k]

# Force sys.path to have our own directory first, in case we want to import from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Must set this env var *before* importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'errorbucket.settings'

import django.core.handlers.wsgi
from django.core.signals import got_request_exception
import django.db
import django.dispatch.dispatcher

def log_exception(*args, **kwds):
   logging.exception('Exception in request:')

got_request_exception.connect(log_exception) # Log errors.
got_request_exception.disconnect(django.db._rollback_on_exception) # Unregister the rollback event handler.


def main():
  util.run_wsgi_app(django.core.handlers.wsgi.WSGIHandler())

if __name__ == '__main__':
  main()

from google.appengine.ext import webapp
from django.utils import simplejson
from auth import http_auth_required
from errorbucket.buckets.models import Bucket

CREDENTIALS = {'heroku': 'cf6d0d056bb08b03'}

class ResourcesHandler(webapp.RequestHandler):
  @http_auth_required(CREDENTIALS)
  def post(self):
    bucket = Bucket.create()
    result = { 'id': bucket.key().name(),
      'config': { 
        'ERRORBUCKET_URL': "http://%s@%s/buckets/%s" % (bucket.secret_key, self.request.headers['HOST'], bucket.key().name()),
      }
    }
    self.response.out.write(simplejson.dumps(result))
    self.response.headers.add_header("Content-Type", "application/json")

class ResourceHandler(webapp.RequestHandler):
  @http_auth_required(CREDENTIALS)
  def delete(self, key_name):
    bucket = Bucket.get_by_key_name(key_name)
    if bucket:
      bucket.delete()
      self.response.out.write('ok')
    else:
      self.response.set_status(404)

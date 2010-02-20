from google.appengine.ext import webapp
from django.utils import simplejson
from decorators import http_auth_required
from bucket.models import Bucket, Error

CREDENTIALS = {'heroku': '5da6fe44c3cc5c28'}

class ResourcesHandler(webapp.RequestHandler):
  @http_auth_required(CREDENTIALS)
  def post(self):
    bucket = Bucket.put_new()
    result = { 'id': bucket.key().name(), 'config': { 'BUCKET_SECRET_KEY': bucket.secret_key } }
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
      self.response.out.write('error')
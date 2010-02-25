from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from google.appengine.api import users
from google.appengine.ext import db
from errorbucket.buckets.models import Bucket, Error
from errorbucket.util import RequestHandler, gae_processor
from auth import parse_auth
  
class UserBucketHandler(RequestHandler):
  def get(self, request):
    user = users.get_current_user()
    bucket = db.GqlQuery("SELECT * FROM Bucket WHERE user = :1", user).get()
    if not bucket:
      bucket = Bucket.create(user=user)
    errors = bucket.error_set.order('-created_at').fetch(30)
    return render_to_response('bucket.html', gae_processor(request, locals()))
    
class ErrorHandler(RequestHandler):
  def post(self, request):
    user = users.get_current_user()
    bucket = db.GqlQuery("SELECT * FROM Bucket WHERE user = :1", user).get()

    if not bucket:
      username, password = parse_auth(self.request)
      bucket = db.GqlQuery("SELECT * FROM Bucket WHERE secret_key = :1", password).get()

    if not bucket:
      self.response.status_code = '401'
      self.response.content = '401 - unauthorized'
      return self.response

    if self.request.META['CONTENT_TYPE'] == 'application/x-www-form-urlencoded':
      message = self.request.POST['message']
    else:
      message = self.request.raw_post_data
    Error(bucket=bucket, message=message).put()

    if self.format() == 'json':
      return HttpResponse(simplejson.dumps({'result': True}), mimetype='application/json')
    return HttpResponseRedirect('/bucket')
    
  def delete(self, request, key):
    error = Error.get(db.Key(key))
    
    user = users.get_current_user()
    bucket = db.GqlQuery("SELECT * FROM Bucket WHERE user = :1", user).get()
    
    if not bucket:
      username, password = parse_auth(self.request)
      bucket = db.GqlQuery("SELECT * FROM Bucket WHERE secret_key = :1", password).get()

    if not bucket or (error.bucket.key() != bucket.key()):
      self.response.status_code = '401'
      self.response.content = '401 - unauthorized'
      return self.response

    error.delete()
    return HttpResponseRedirect('/bucket')

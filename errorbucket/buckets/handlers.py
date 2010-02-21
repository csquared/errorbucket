from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from google.appengine.api import users
from google.appengine.ext import db
from errorbucket.buckets.models import Bucket, Error
from errorbucket.util import RequestHandler, gae_processor
  
class UserBucketHandler(RequestHandler):
  def get(self, request):
    user = users.get_current_user()
    bucket = db.GqlQuery("SELECT * FROM Bucket WHERE user = :1", user).get()
    if not bucket:
      bucket = Bucket.create(user=user)
    errors = bucket.error_set.order('-created_at').fetch(30)
    return render_to_response('bucket.html', gae_processor(request, locals()))
    
class BucketHandler(RequestHandler):
  def post(self, request, key_name):
    bucket = Bucket.get_by_key_name(key_name)
    if not bucket:
      self.response.status_code = '404'
      self.response.content = '404 - not found'
      return self.response
    
    if not request.POST.has_key('secret_key') or request.POST['secret_key'] != bucket.secret_key:
      self.response.status_code = '401'
      self.response.content = '401 - unauthorized'
      return self.response
      
    Error(bucket=bucket, message=self.request.POST['message']).put()
    if self.format() == 'json':
      return HttpResponse(simplejson.dumps({'success': True}), mimetype='application/json')
    return HttpResponseRedirect('/bucket')
    
class BucketsHandler(RequestHandler):
  pass

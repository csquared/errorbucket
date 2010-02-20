from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from google.appengine.api import users
from google.appengine.ext import db

from errorbucket.buckets.models import Bucket, Error


def index(request):
  return HttpResponse('buckets')

def gae_processor(request, data):
  # FIXME: why is RequestContext with processor not working?!
  data.update({
    'request': request,
    'user': users.get_current_user(),
    'login_url': users.create_login_url("/bucket"),
    'logout_url': users.create_logout_url("/"),
  })
  return data
  
def user_bucket(request):
  user = users.get_current_user()
  bucket = db.GqlQuery("SELECT * FROM Bucket WHERE user = :1", user).get()
  if not bucket:
    bucket = Bucket.create(user=user)
  errors = bucket.error_set.fetch(30)
  return render_to_response('bucket.html', gae_processor(request, {
    'bucket': bucket,
    'errors': errors,
  }))
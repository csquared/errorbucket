from django.http import HttpResponse
from django.shortcuts import render_to_response
from google.appengine.api import users

def index(request):
  return render_to_response('index.html', {
    'user': users.get_current_user(),
    'login_url': users.create_login_url("/bucket"),
    'logout_url': users.create_logout_url("/"),
  })
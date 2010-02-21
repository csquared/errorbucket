from django.http import HttpResponse, HttpResponseServerError
from google.appengine.api import users

def gae_processor(request, data):
  """
  Mixes in Google App Engine auth into the template context.
  FIXME: why is RequestContext with this processor not working?!
  """
  data.update({
    'request': request,
    'user': users.get_current_user(),
    'login_url': users.create_login_url("/bucket"),
    'logout_url': users.create_logout_url("/"),
  })
  return data
  
class RequestHandler(object):
  def __call__(self, request, *args, **kwargs):
    self.request = request
    self.response = HttpResponse()
    method = request.META['REQUEST_METHOD'].lower()
    handler = getattr(self, method, None)
    if handler is None:
      raise Exception('%s method not defined' % method)
    return handler(request, *args, **kwargs)
    
  def format(self):
    accept = self.request.META.get('HTTP_ACCEPT', '')
    if 'application/json' in accept:
      return 'json'
    if 'application/xml' in accept:
      return 'xml'
    if 'text/plain' in accept:
      return 'text'
    return 'html'
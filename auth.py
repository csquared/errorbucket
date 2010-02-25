import base64
from google.appengine.ext.webapp import Response

class http_auth_required(object):
  """
  A decorator to handle basic HTTP authentication. Takes a dictionary of
  username: password pairs to authenticate against.
  """
  def __init__(self, credentials):
    self.credentials = credentials

  def __call__(self, method):
    def inner(inst, *args, **kwargs):
      username, password = parse_auth(inst.request)
      if self.credentials.has_key(username) and self.credentials[username] == password:
        inst.request.headers['REMOTE_USER'] = username
        return method(inst, *args, **kwargs)

      # The credentials are incorrect, or not provided; challenge for username/password
      inst.response.set_status(401)
      inst.response.headers.add_header("WWW-Authenticate", 'Basic realm="restricted"')

    return inner

def parse_auth(request):
  # header indicates login attempt
  try:
    authorization = request.headers['AUTHORIZATION'] # gae request
  except AttributeError:
    authorization = request.META['HTTP_AUTHORIZATION'] # django request

    auth = authorization.split()
    if len(auth) == 2 and auth[0].lower() == 'basic':
        username, password = base64.b64decode(auth[1]).split(':')
        return username, password
  return None, None
from uuid import uuid4
from google.appengine.ext import db
from django.utils import simplejson

class Bucket(db.Model):
  user = db.UserProperty()
  secret_key = db.StringProperty(required=True)
  created_at = db.DateTimeProperty(auto_now_add=True)

  @classmethod
  def create(cls, user=None):
    randomness = str(uuid4()).split("-")
    key_name = randomness[0]
    secret_key = randomness[-1]
    bucket = Bucket(key_name=key_name, user=user, secret_key=secret_key)
    bucket.put()
    return bucket
    
  def to_dict(self):
    return {
      'key': self.key().name(),
      'secret_key': self.secret_key,
    }

  def to_json(self):
    return simplejson.dumps(self.to_dict())

class Error(db.Model):
  bucket = db.ReferenceProperty(Bucket, required=True)
  message = db.StringProperty()
  created_at = db.DateTimeProperty(auto_now_add=True)
  
  def to_dict(self):
    return {
      'message': self.message,
      'created_at': self.created_at,
    }
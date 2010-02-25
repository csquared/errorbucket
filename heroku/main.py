#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from heroku.handlers import ResourcesHandler, ResourceHandler
  
def main():
  application = webapp.WSGIApplication([
    ('/heroku/resources', ResourcesHandler),
    ('/heroku/resources/(.*?)', ResourceHandler),
  ], debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()


import os
import sys
import jinja2
import webapp2 
import urllib2
from gaeoauth import OAuthHandler, OAuthClient
from checkLink import CheckLink

from datetime import datetime, timedelta
from hashlib import sha1
from hmac import new as hmac
from os.path import dirname, join as join_path
from random import getrandbits
from time import time
from urllib import urlencode, quote as urlquote
from uuid import uuid4
from wsgiref.handlers import CGIHandler

sys.path.insert(0, join_path(dirname(__file__), 'lib')) # extend sys.path

from demjson import decode as decode_json

from google.appengine.api.urlfetch import fetch as urlfetch, GET, POST
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# ------------------------------------------------------------------------------
# The core of who tweeted this?
# fetches tweets from users' timeline and check them against the submitted url
# ------------------------------------------------------------------------------


class MainHandler(webapp2.RequestHandler):
    """Demo Twitter App."""

    # def __init__(self, request, response):
    #      self.initialize(request, response)
    #      self.cache = {}
    #      self.statusCache = {}
    #      self.longUrls = {}      
 
    def get(self, service):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write('Hello, webapp!')

        self.cache = {}
        self.statusCache = {}
        self.longUrls = {}      
        self.template_values = {}
        self.client = OAuthClient('twitter', self)

        link = self.request.get('url')

        if not self.client.get_cookie():
            self.template_values['logged'] = False
        else:
          self.template_values['logged'] = True
          
          info = self.client.get('/account/verify_credentials')
          self.template_values['info'] = info
          
          # rate_info = self.client.get('/account/rate_limit_status')
          # write("<strong>API Rate Limit Status:</strong> %r" % rate_info)
          
          if "" != link:
            self.template_values['link'] = link
            
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(self.template_values))


app = webapp2.WSGIApplication([
         ('/oauth/(.*)/(.*)', OAuthHandler),
         ('/link/(.*)', CheckLink),
         ('/(.*)', MainHandler)
         ], debug=True)

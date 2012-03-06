import os
import sys
import jinja2
import webapp2 
import urllib2

from urlparse import urlparse
from gaeoauth import OAuthHandler, OAuthClient

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


class CheckLink(webapp2.RequestHandler):

    # def __init__(self):


    def get(self, link):
      
      self.cache = {}

      self.client = OAuthClient('twitter', self)

      if not self.client.get_cookie():
          self.response.out.write("NEEDLOGIN")
          return
      
      page = self.request.get('page')
      print "Page " + page
      
      if isinstance(page, int):
        self.queryTwitter(link, page)
      else:
        self.queryTwitter(link, 1)

    def queryTwitter(self,link,x):
        write = self.response.out.write;

        print "looking up" + link
        print "Page " + str(x)

        statuses = self.client.get('/statuses/home_timeline',page=x,include_entities="true")
        for status in statuses:
            entities = status['entities']
            print status['id']
            urls = entities['urls']
            # print urls
            if urls:
                for url in urls:
                    # print url
            
                    # statusId = status['id']
                    # self.statusCache[statusId] = status

                    # BAD OPTIMISATION !
                    # if the net location of the url is longer than 10 chars
                    # no need to check if the url is a redirect
                    # if len(urlparse(url['expanded_url']).netloc) > 10 :
                    expandedUrl = self.unshorten(url['expanded_url'])
                    # else:
                    #   expandedUrl = url['expanded_url']

                    print expandedUrl
                  
                    if expandedUrl == link:
                      print "YAY"
                      # USER/status/STATUS_ID
                      tweet = status['user']['screen_name']+"/status/"+ str(status['id'])
                      write(str(tweet))
                      return
                    # self.longUrls[expandedUrl] = statusId
            
        write("")

    def unshorten(self, url):
      try:
        result = self.cache.get(url)
        if result is None:
          result = urllib2.urlopen(url).geturl()
          self.cache[url] = result
      except urllib2.HTTPError:
          result = "URL Doesn't exist"
      except ValueError:
          result = "Invalid Url"
      return result

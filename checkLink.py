import os
import sys
import jinja2
import webapp2 
import urllib
import urllib2
import httplib

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

def num (s):
    try:
        return int(s)
    except exceptions.ValueError:
        return s



class CheckLink(webapp2.RequestHandler):

    # def __init__(self):


    def get(self, link):
      
      self.cache = {}

      self.client = OAuthClient('twitter', self)

      if not self.client.get_cookie():
          self.response.out.write("NEEDLOGIN")
          return
      
      page = num(self.request.get('page'))
      
      if isinstance(page, ( int, long )):
        self.queryTwitter(link, page)
      else:
        self.queryTwitter(link, 1)

    def queryTwitter(self,link,x):
        write = self.response.out.write;

        print "looking up, Page " + str(x) + " for " + link

        try:
          statuses = self.client.get('/statuses/home_timeline',page=x,include_entities="true")
#         except DeadlineExceededError:
        except Exception: 
          print "Big bad exception. Trying again"
          self.queryTwitter(link, x)
          return
        
        # there are 20 tweets in a page
        # print "Status # " + str(len(statuses))
        for status in statuses:
            entities = status['entities']
            # print status['id']
            urls = entities['urls']
            # print urls
            if urls:
                for url in urls:
                    # print url
            
                    # statusId = status['id']
                    # self.statusCache[statusId] = status

                    # BAD OPTIMISATION !
                    # if the net location of the url is longer than 20 chars
                    # no need to check if the url is a redirect
                    # if len(urlparse(url['expanded_url']).netloc) > 20 :
                    unshortenThis = url['expanded_url']
                    if unshortenThis is not None:
                        print "- to unshorten: " + unshortenThis
                    
                        expandedUrl = self.unshorten_url(unshortenThis)
                        # else:
                        #   expandedUrl = url['expanded_url']

                        print "-> " + expandedUrl
                  
                        if self.same_urls(expandedUrl,link):
                          print "YAY"
                          # USER/status/STATUS_ID
                          tweet = status['user']['screen_name']+"/status/"+ str(status['id'])
                          write('{"page":"'+str(x)+'","url":"'+ str(tweet) +'"}')
                          return
                        # self.longUrls[expandedUrl] = statusId
            
        write('{"page":"'+str(x)+'","url":""}')

    def unshorten(self, url, trialNumber=1):
      if (trialNumber>3):
          return ""
      try:
        result = self.cache.get(url)
        if result is None:
          result = urllib2.urlopen(url,timeout=10).geturl()
          self.cache[url] = result
      except urllib2.HTTPError, error:
          print "HTTPError " + error.read()
          result = "HTTPError"
      except httplib.HTTPException:
          # in this case we should probably just try again
          result = "no clue what is going on, tried " + str(trialNumber) + " times."
          self.unshorten(url,trialNumber+1)
      except ValueError:
          result = "Invalid Url"
      except AttributeError:
          print "AttributeError " + url

      return result

    def canonical_url(self, u):
      # u = u.lower()
      if u.startswith("http://"):
          u = u[7:]
      if u.startswith("www."):
          u = u[4:]
      while u.endswith("/"):
          u = u[:-1]
      return u

    def same_urls(self, u1, u2):
      return self.canonical_url(u1) == self.canonical_url(u2)

    # This is for Py2k.  For Py3k, use http.client and urllib.parse instead, and
    # use // instead of / for the division

    def unshorten_url(self,url,trialNumber=1):
        _, host, path, _, _ = urllib2.urlparse.urlsplit(url)
        # print host, path
        h = httplib.HTTPConnection(host)
        h.request('HEAD', path)
        try:
          response = h.getresponse()
          print str(response.status) + " " + response.reason 
          if response.status/100 == 3 and response.getheader('Location'):
              return response.getheader('Location')
          elif response.status/100 == 4:
              return self.unshorten(url)
          else:
              return url
        except:
          if (trialNumber<3):
            return self.unshorten_url(url,trialNumber+1)
          else:
            return self.unshorten(url)
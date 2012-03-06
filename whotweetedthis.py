#!/usr/bin/python
import pprint
import urllib
import urllib2
import simplejson
import tweepy
import urlparse
from twitterKeys import TwitterKeys 
from tweepy.cursor import Cursor

print "Content-type: text/html\n\n"

class WhoTweetedThis(object):

  def __init__(self):
    self.authenticate(TwitterKeys())
    self.cache = {}

  # == OAuth Authentication ==
  def authenticate(self, keys):
    # This mode of authentication is the new preferred way
    # of authenticating with Twitter.

    self.auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    self.auth.set_access_token(keys.access_token, keys.access_token_secret)

  def parseTweets(self):
    api = tweepy.API(self.auth)

    # If the authentication was successful, you should
    # see the name of the account print out
    print api.me().name      

    # page = 1
    for x in range(1,5):
      print "Page " + str(x)
      statuses = api.home_timeline(page=x,include_entities="true")
      for status in statuses:
        json = status._json
        # print json
        for prop, attrib in json.items():
          if prop == "entities":
            for p, a in attrib.items():
              if p == "urls":
                for urls in a:
                  print json.get('id')
                  print urls['expanded_url']
                  print urlparse.urlparse(urls['expanded_url'])
                  
                  for i in self.unshorten(urls['expanded_url']):
                    print "unshortened: " + i
          
          
  # def unshorten_url(self, url):
  #     parsed = urlparse.urlparse(url)
  #     h = httplib.HTTPConnection(parsed.netloc)
  #     h.request('HEAD', parsed.path)
  #     response = h.getresponse()
  #     if response.status/100 == 3 and response.getheader('Location'):
  #         return response.getheader('Location')
  #     else:
  #         return url


  def unshorten(self, url):
    # start_response('200 OK', [('Content-type','text/plain')])
    # url = environ['PATH_INFO'].lstrip('/')
    # yield 'Looking up: ' + url + '...'
    try:
      result = self.cache.get(url)
      if result is None:
        result = urllib2.urlopen(url).geturl()
        self.cache[url] = result
    except urllib2.HTTPError:
      result = "URL Doesn't exist"
    except ValueError:
      result = "Invalid Url"
    yield result
    
app = WhoTweetedThis()
app.parseTweets()
import os
import sys
import urllib2
import md5
import logging
from google.appengine.api import memcache
from google.appengine.api import urlfetch

class CacheUtil:

    @staticmethod
    def getCachedResponse(url):
        cache_ttl = 60*60

        logging.getLogger().setLevel(logging.DEBUG)   

        key = md5.new(url).hexdigest()
        res = memcache.get(key)
        if res is not None:
            logging.debug('Cached response (%s): %s', key, res)

            return res
        else:
            res = urlfetch.fetch(url, deadline=10).content
            logging.debug('Caching response (%s): %s', key, res)
            memcache.add(key, res, cache_ttl)
            
            return res
        
    
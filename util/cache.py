import os
import sys
import urllib2
import md5
import logging
from google.appengine.api import memcache
from google.appengine.api import urlfetch

class CacheUtil:

    @staticmethod
    def getCachedResponse(url, cache=True, ttl=60*60*24):

        logging.getLogger().setLevel(logging.DEBUG)   

        key = md5.new(url).hexdigest()
        res = None
        if cache:
        	res = memcache.get(key)
        if res is not None:
            logging.debug('Cached response (%s): %s', key, res)

            return res
        else:
            res = urlfetch.fetch(url, deadline=20).content
            logging.debug('Caching response (%s): %s', key, res)
            memcache.add(key, res, ttl)
            
            return res

    @staticmethod
    def getCachedContent(key, cache=True):

        logging.getLogger().setLevel(logging.DEBUG)   

        key = md5.new(key).hexdigest()
        data = None
        if cache:
            data = memcache.get(key)
        if data is not None:
            logging.debug('Cached content (%s): %s', key, data)
            
        return data

    @staticmethod
    def setCachedContent(key, data, ttl=60*60*24):

        logging.getLogger().setLevel(logging.DEBUG)   

        key = md5.new(key).hexdigest()
        logging.debug('Caching content (%s): %s', key, data)
        memcache.set(key, data, ttl)
        
    
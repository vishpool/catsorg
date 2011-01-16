import os
import urllib2
import string
import md5
import logging
from django.utils import simplejson as json

from admin import admin
from google.appengine.api import memcache

class PetFinderAPI:
    base = 'http://api.petfinder.com/'
    token = None
    cache_ttl = 1*60
    
    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)        
        
    def getShelterPets(self):
        data = {'id': self.getShelterID()}
        res = self.getResponse('shelter.getPets', data)
    
        return res
        
    def getResponse(self, method, data):
        params = self.getParams(data)
        signed = self.getSigned(params)
        url = self.base + method + '?' + signed

        key = md5.new(url).hexdigest()
        res = memcache.get(key)
        if res is not None:
            logging.debug('Cached response (%s): %s', key, res)

            return res
        else:
            res = json.loads(urllib2.urlopen(url).read())
            logging.debug('Caching response (%s): %s', key, res)
            memcache.add(key, res, self.cache_ttl)
            
            return res
        
    def getSigned(self, params):
        return params + '&sig=' + md5.new(self.getApiSecret() + params).hexdigest()

    def getToken(self):
        data = {}
        res = self.getResponse('auth.getToken', data)
        token = res['petfinder']['auth']['token']

        return token

    def getParams(self, data):
        params = 'key=' + self.getApiKey()
        for d in data: 
            params += '&' + d + '=' + data[d]
        
        return params + '&format=json'
            
    def getApiKey(self):
        shelter = admin.Shelter.get_by_key_name('shelter')
        logging.debug(shelter)

        return shelter.api_key

    def getApiSecret(self):
        shelter = admin.Shelter.get_by_key_name('shelter')

        return shelter.api_secret

    def getShelterID(self):
        shelter = admin.Shelter.get_by_key_name('shelter')

        return shelter.shelter_id


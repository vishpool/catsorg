import os
import urllib2
import string
import md5
import logging
from django.utils import simplejson as json

from admin import admin

class PetFinderAPI:
    base = 'http://api.petfinder.com/'
    token = None 
    
    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)
        self.token = self.getCachedToken()
        
        
    def getShelterPets(self):
        data = {'id': self.getShelterID()}
        res = self.getResponse('shelter.getPets', data)
    
        return res
        
    def getResponse(self, method, data):
        params = self.getParams(data)
        signed = self.getSigned(params)
        url = self.base + method + '?' + signed
        
        return json.loads(urllib2.urlopen(url).read())
        
    def getSigned(self, params):
        return params + '&sig=' + md5.new(self.getApiSecret() + params).hexdigest()

    def getToken(self):
        if self.token is not None:
            return self.token
            
        data = {}
        res = self.getResponse('auth.getToken', data)
        
        return res['petfinder']['auth']['token']

    def getCachedToken(self):
        return self.getToken()
    
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


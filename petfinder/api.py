import os
import sys
import urllib2
import string
import md5
import logging
from django.utils import simplejson as json
from google.appengine.api import memcache

from admin.models import *

class PetFinderAPI:
    base = 'http://api.petfinder.com/'
    token = None
    cache_ttl = 5*60
    
    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)        
        
    def getShelterPets(self, offset = 0, count = 25):
        data = {'id': self.getShelterID(),
                'count': count,
                'offset': offset}
        res = self.getResponse('shelter.getPets', data)
        
        pets = []
        for pet in res['petfinder']['pets']['pet']:
            logging.debug('Parsing pet: %s', pet)
            pet = {'id': pet['id']['$t'],
                'name': pet['name']['$t'],
                'description': pet['description']['$t'],
                'animal': self.getAnimal(pet),
                'breeds': self.getBreeds(pet),
                'age': pet['age']['$t'],
                'size': self.getSize(pet),
                'sex': self.getSex(pet),
                'photos': self.getPhotos(pet)}

            logging.debug('Parsed pet: %s', pet)
            pets.append(pet)
            
        return pets
    
    def getAnimal(self, pet):
        if pet['animal']:
            return pet['animal']['$t']
        
        return ''
                
    def getBreeds(self, pet):
        breeds = []
        
        if pet['breeds']:
            if type(pet['breeds']['breed']) is list:
                for breed in pet['breeds']['breed']:
                    breeds.append(breed['$t'])
            else:
                breeds.append(pet['breeds']['breed']['$t'])
        
        return breeds
    
    def getPhotos(self, pet):
        photos = {}
        if 'photo' in pet['media']['photos'].keys():
            for photo in pet['media']['photos']['photo']:
                if photo['@id'] not in photos.keys():
                    photos[photo['@id']] = {photo['@size']: photo['$t']}
                else:
                    photos[photo['@id']][photo['@size']] = photo['$t']

        return photos
    
    def getSize(self, pet):
        size = pet['size']['$t']
        if size == 'S':
            return 'Small'
        elif size == 'M':
            return 'Medium'
        elif size == 'L':
            return 'Large'
        
        return size

    def getSex(self, pet):
        sex = pet['sex']['$t']
        if sex == 'F':
            return 'Female'
        elif sex == 'M':
            return 'Male'
        
        return sex
    
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
            params += '&' + d + '=' + str(data[d])
        
        return params + '&format=json'
            
    def getApiKey(self):
        shelter = Shelter.get_by_key_name('shelter')
        logging.debug(shelter)

        return shelter.api_key

    def getApiSecret(self):
        shelter = Shelter.get_by_key_name('shelter')

        return shelter.api_secret

    def getShelterID(self):
        shelter = Shelter.get_by_key_name('shelter')

        return shelter.shelter_id


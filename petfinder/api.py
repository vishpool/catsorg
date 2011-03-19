import os
from google.appengine.dist import use_library
use_library('django', '1.2')
import sys
import urllib2
import md5
import logging
import re
import pickle
from django.utils import simplejson as json

from admin.models import *
from util import *

class PetFinderAPI:
    base = 'http://api.petfinder.com/'
    token = None
    shelter = None
    
    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)        
        
    def getShelterPets(self, offset = 0, count = 25):

        data = {
            'id': self.getShelterID(),
            'count': count,
            'offset': offset}
        
        res = self.getResponse('shelter.getPets', data)
        
        pets = []
        for pet in res['petfinder']['pets']['pet']:
            cpet = CacheUtil.getCachedContent('pet-' + str(pet['id']['$t']))
            if cpet is not None:
                pet = cpet
            else:
                petDB = Pet(key_name=str(pet['id']['$t']),
                    pet_id=str(pet['id']['$t']),
                    pet_data=pet)
                Pet.save(petDB)

                pet = {
                    'id': pet['id']['$t'],
                    'name': pet['name']['$t'],
                    'description': self.getDescription(pet['description']['$t']),
                    'animal': self.getAnimal(pet),
                    'breeds': self.getBreeds(pet),
                    'age': pet['age']['$t'],
                    'size': self.getSize(pet),
                    'sex': self.getSex(pet),
                    'photos': self.getPhotos(pet)}

                logging.debug('Parsed pet: %s', pet)
                CacheUtil.setCachedContent('pet-' + str(pet['id']), pet);

            pets.append(pet)

                    
        return pets
    
    def getShelterPet(self, pet_id):

        pet = CacheUtil.getCachedContent('pet-' + pet_id)
        if pet is not None:
            return pet
        else:
#             data = {
#                 'id': pet_id,
#                 'token': self.getToken()}
#         
#             pet = self.getResponse('pet.get', data)
#             Workaround for pet.get
            petDB = Pet.get_by_key_name(pet_id)
            pet = petDB.pet_data
            if pet is not None: 
                pet = {
                    'id': pet['id']['$t'],
                    'name': pet['name']['$t'],
                    'description': self.getDescription(pet['description']['$t']),
                    'animal': self.getAnimal(pet),
                    'breeds': self.getBreeds(pet),
                    'age': pet['age']['$t'],
                    'size': self.getSize(pet),
                    'sex': self.getSex(pet),
                    'photos': self.getPhotos(pet)}
    
                logging.debug('Parsed pet: %s', pet)
                CacheUtil.setCachedContent('pet-' + str(pet['id']), pet);

        return pet

    def getDescription(self, desc):
        desc = re.sub('</?(form|input|center|h5|p|font)*>', '', desc.partition('<form')[0])
        return desc

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
                if int(photo['@id']) not in photos.keys():
                    photos[int(photo['@id'])] = {photo['@size']: photo['$t']}
                else:
                    photos[int(photo['@id'])][photo['@size']] = photo['$t']
                if photo['@size'] == 'x':
                    photos[int(photo['@id'])]['info'] = ImageUtil.getImageInfo(photo['$t'])
            
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
        
        return json.loads(CacheUtil.getCachedResponse(url))

    def getSigned(self, params):
        return params + '&sig=' + md5.new(self.getApiSecret() + params).hexdigest()

    def getToken(self):
        if self.token is None:
            data = {}
            res = self.getResponse('auth.getToken', data)
            self.token = res['petfinder']['auth']['token']['$t']

        return self.token

    def getParams(self, data):
        params = 'key=' + self.getApiKey()
        for d in data: 
            params += '&' + d + '=' + str(data[d])
        
        return params + '&format=json'
        
    def setShelter(self):
        if self.shelter is None:
            self.shelter = Shelter.get_by_key_name('shelter')
            
        if self.shelter is None:
            sys.exit('No shelter found!')

            
    def getApiKey(self):
        self.setShelter();

        return self.shelter.api_key

    def getApiSecret(self):
        self.setShelter();

        return self.shelter.api_secret

    def getShelterID(self):
        self.setShelter();

        return self.shelter.shelter_id

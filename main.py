import os
from google.appengine.dist import use_library
use_library('django', '1.2')
import logging
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from admin.models import *
from petfinder.api import *
from util import *

template.register_template_library('templatetags.custom_tags')

class MainHandler(webapp.RequestHandler):
    
    @staticmethod
    def getMainValues(request):

        shelter = CacheUtil.getCachedContent('shelter')
        if shelter is None:
            shelter = Shelter.get_by_key_name('shelter')
            CacheUtil.setCachedContent('shelter', shelter)

        values = {
            'site_title': shelter.site_title,
            'site_footer': shelter.site_footer,
            'shelter_name': shelter.shelter_name,
            'shelter_phone': shelter.shelter_phone,
            'shelter_email': shelter.shelter_email,
            'shelter_email_donations': shelter.shelter_email_donations,
            'shelter_address': shelter.shelter_address,
            'site_news': shelter.site_news,
            'site_about_us_mission': shelter.site_about_us_mission,
            'site_about_us_who': shelter.site_about_us_who,
            'site_contact_us_emails': shelter.site_contact_us_emails,
            'shelter_facebook': shelter.shelter_facebook,
            'shelter_twitter': shelter.shelter_twitter,
            'shelter_twitter_user': os.path.basename(shelter.shelter_twitter),
            'google_analytics': shelter.google_analytics,
            'site_url': 'http://' + request.headers.get('Host'),
            'url': request.url,
            'logo': 'http://' + request.headers.get('Host') + '/images/logo_main.png'
        }
        
        return values

    def get(self, req, page):

        api = PetFinderAPI()
        pets = api.getShelterPets()
        pets = pets[0:3]

        values = {
            'page': page,
            'nav': 'index',
            'title': 'Home',
            'css': 'styles.css',
            'page_class': '',
            'pets': pets,
        }
        values = dict(values, **MainHandler.getMainValues(self.request))
        
        if req == None:
            req = 'index.html'

        path = os.path.join(os.path.dirname(__file__), req)
        self.response.out.write(template.render(path, values))

class AdoptionsHandler(webapp.RequestHandler):

    def get(self, req, page):

        api = PetFinderAPI()
        pets = api.getShelterPets()
        featured = random.sample(pets, 4)
        pets = pets[0:12]

        values = {
            'page': page,
            'nav': 'adoptions',
            'title': 'Adoptions',
            'css': 'adoptions.css',
            'page_class': 'adoptions',
            'featured': featured,
            'pets': pets
        }
        values = dict(values, **MainHandler.getMainValues(self.request))

        path = os.path.join(os.path.dirname(__file__), req)
        self.response.out.write(template.render(path, values))

class AdoptionsPetHandler(webapp.RequestHandler):

    def get(self, req, page, slug, pet_id):

        api = PetFinderAPI()
        pet = api.getShelterPet(pet_id)

        logging.debug(self.request)
        values = {
            'page': page,
            'nav': 'adoptions',
            'title': 'Adoptions - ' + pet['animal'] + ' - ' + pet['name'],
            'css': 'adoptions_pet.css',
            'page_class': 'adoptions',
            'pet': pet,
        }
        if self.request.headers.get('Referer') is not None and self.request.headers.get('Host') in self.request.headers.get('Referer') and 'adoptions.html' in self.request.headers.get('Referer'):
            values['back'] = True
        values = dict(values, **MainHandler.getMainValues(self.request))

        path = os.path.join(os.path.dirname(__file__), 'adoptions_pet.html')
        self.response.out.write(template.render(path, values))

class ApplicationHandler(webapp.RequestHandler):

    def get(self, req, page, petm, slug, pet_id):

        pet = None
        if petm is not None:
            api = PetFinderAPI()
            pet = api.getShelterPet(pet_id)

        values = {
            'page': page,
            'nav': 'adoptions',
            'title': 'Adoption Application',
            'css': 'adoptions_pet.css',
            'page_class': 'application',
            'pet': pet,
        }
        if pet is not None:
            logging.debug(pet)
            values['title'] += ' - ' + pet['animal'] + ' - ' + pet['name']
            
        values = dict(values, **MainHandler.getMainValues(self.request))

        path = os.path.join(os.path.dirname(__file__), 'application.html')
        self.response.out.write(template.render(path, values))

class DonationsHandler(webapp.RequestHandler):

    def get(self, req, page):

        values = {
            'page': page,
            'nav': 'donations',
            'title': 'Donations',
            'css': 'donations.css',
            'page_class': 'donations'
        }
        values = dict(values, **MainHandler.getMainValues(self.request))

        path = os.path.join(os.path.dirname(__file__), req)
        self.response.out.write(template.render(path, values))

class AboutUsHandler(webapp.RequestHandler):

    def get(self, req, page):

        values = {
            'page': page,
            'nav': 'about_us',
            'title': 'About Us',
            'css': 'about_us.css',
            'page_class': 'aboutUs'
        }
        values = dict(values, **MainHandler.getMainValues(self.request))

        path = os.path.join(os.path.dirname(__file__), req)
        self.response.out.write(template.render(path, values))

class ContactUsHandler(webapp.RequestHandler):

    def get(self, req, page):

        values = {
            'page': page,
            'nav': 'contact_us',
            'title': 'Contact Us',
            'css': 'contact_us.css',
            'page_class': 'contactUs'
        }
        values = dict(values, **MainHandler.getMainValues(self.request))

        path = os.path.join(os.path.dirname(__file__), req)
        self.response.out.write(template.render(path, values))

def main():

    logging.getLogger().setLevel(logging.DEBUG)

    application = webapp.WSGIApplication([('/((index).html)?', MainHandler),
                                          ('/((adoptions|adoptions_success).html)', AdoptionsHandler),
                                          ('/((adoptions)-(.+)-(\d+).html)', AdoptionsPetHandler),
                                          ('/((application)(-(.+)-(\d+))?.html)', ApplicationHandler),
                                          ('/((donations|donations_success).html)', DonationsHandler),
                                          ('/((about_us).html)', AboutUsHandler),
                                          ('/((contact_us).html)', ContactUsHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
#
import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from petfinder.api import *
import random

class MainHandler(webapp.RequestHandler):
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
            'news': 'Some News Here'
        }
        
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

        path = os.path.join(os.path.dirname(__file__), req)
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

        path = os.path.join(os.path.dirname(__file__), req)
        self.response.out.write(template.render(path, values))

def main():
    logging.getLogger().setLevel(logging.DEBUG)

    application = webapp.WSGIApplication([('/((index).html)?', MainHandler),
                                          ('/((adoptions).html)', AdoptionsHandler),
                                          ('/((donations|donations_success).html)', DonationsHandler),
                                          ('/((about_us).html)', AboutUsHandler),
                                          ('/((contact_us).html)', ContactUsHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

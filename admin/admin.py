#!/usr/bin/env python
#
import os
import logging
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from petfinder.api import PetFinderAPI

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        shelter = Shelter.get_by_key_name('shelter')

        if shelter is not None:
            template_values = {
                'admin': user.nickname(),
                'shelter_admin': shelter.shelter_admin.nickname() + ' at ' + shelter.updated.isoformat(),
                'shelter_id': shelter.shelter_id,
                'site_title': shelter.site_title,
                'site_footer': shelter.site_footer,
                'api_key': shelter.api_key,
                'api_secret': shelter.api_secret,
            }
        else:
            template_values = {
                'admin': user.nickname(),
                'shelter_admin': user.nickname(),
                'shelter_id': '',
                'site_title': '',
                'site_footer': '',
                'api_key': '',
                'api_secret': '',
            }


        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
    
        action = self.request.get('submit')
        
        if action == 'Get Pets':
            api = PetFinderAPI()
            logging.debug(self.request)
            pets = api.getShelterPets()

            for p in pets['petfinder']['pets']['pet']:
                pet = '<p><img src="' + p['media']['photos']['photo'][0]['$t'] + '" />'
                self.response.out.write(pet)
                

class Shelter(db.Model):
    shelter_id = db.StringProperty(required=True)
    shelter_admin = db.UserProperty(required=True)
    site_title = db.StringProperty(required=True)
    site_footer = db.StringProperty(required=True)
    api_key = db.StringProperty(required=True)
    api_secret = db.StringProperty(required=True)
    updated = db.DateTimeProperty(auto_now_add=True)

class ShelterSetupHandler(webapp.RequestHandler):
    def post(self):
        shelter = Shelter(key_name='shelter',
                            shelter_id=self.request.get('shelter_id'),
                            shelter_admin=users.get_current_user(),
                            site_title=self.request.get('site_title'),
                            site_footer=self.request.get('site_footer'),
                            api_key=self.request.get('api_key'),
                            api_secret=self.request.get('api_secret'))

        shelter.put()
        self.redirect('/admin/')

def main():
    logging.getLogger().setLevel(logging.DEBUG)

    application = webapp.WSGIApplication([('/admin/?', MainHandler),
                                         ('/admin/shelter', ShelterSetupHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

import os
from google.appengine.dist import use_library
use_library('django', '1.2')
import logging
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from django.utils import simplejson as json

from petfinder.api import *
from util import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        shelter = Shelter.get_by_key_name('shelter')

        if shelter is not None:
            template_values = {
                'shelter_id': shelter.shelter_id,
                'api_key': shelter.api_key,
                'api_secret': shelter.api_secret,
                'shelter_name': shelter.shelter_name,
                'shelter_phone': shelter.shelter_phone,
                'shelter_email': shelter.shelter_email,
                'shelter_email_donations': shelter.shelter_email_donations,
                'shelter_address': shelter.shelter_address,
                'site_title': shelter.site_title,
                'site_footer': shelter.site_footer,
                'site_news': shelter.site_news,
                'site_about_us_mission': shelter.site_about_us_mission,
                'site_about_us_who': shelter.site_about_us_who,
                'site_contact_us_emails': shelter.site_contact_us_emails,
                'shelter_facebook': shelter.shelter_facebook,
                'shelter_twitter': shelter.shelter_twitter,
            }
            template_values['shelter_data'] = json.dumps(template_values)
            template_values['admin'] = user.nickname()
            template_values['shelter_admin'] = shelter.shelter_admin.nickname() + ' at ' + shelter.updated.isoformat()
            
        else:
            template_values = {
                'admin': user.nickname(),
                'shelter_admin': user.nickname(),
                'shelter_id': '',
                'api_key': '',
                'api_secret': '',
                'shelter_name': '',
                'shelter_phone': '',
                'shelter_email': '',
                'shelter_email_donations': '',
                'shelter_address': '',
                'site_title': '',
                'site_footer': '',
                'site_news': '',
                'site_about_us_mission': '',
                'site_about_us_who': '',
                'site_contact_us_emails': '',
                'shelter_facebook': '',
                'shelter_twitter': '',
            }
            template_values['shelter_data'] = json.dumps(template_values)
            template_values['admin'] = user.nickname()
            template_values['shelter_admin'] = user.nickname()

        path = os.path.join(os.path.dirname(__file__), 'admin.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        action = self.request.get('submit')
        
        if action == 'Get Pets':
            api = PetFinderAPI()
            pets = api.getShelterPets()

            for pet in pets:
                logging.debug(pet['id'])
                p = '<a href="http://www.petfinder.com/petdetail/' + str(pet['id']) + '" title="' + pet['name'] + '">'
                if pet['photos']:
                    p += '<img src="' + pet['photos'][1]['t'] + '" />'
                p += '</a>'
                self.response.out.write(p)
                

class ShelterSetupHandler(webapp.RequestHandler):
    def post(self):
        shelter = Shelter(key_name='shelter',
                            shelter_id=self.request.get('shelter_id'),
                            shelter_admin=users.get_current_user(),
                            api_key=self.request.get('api_key'),
                            api_secret=self.request.get('api_secret'),
                            shelter_name=self.request.get('shelter_name'),
                            shelter_phone=self.request.get('shelter_phone'),
                            shelter_address=self.request.get('shelter_address'),
                            shelter_email=self.request.get('shelter_email'),
                            shelter_email_donations=self.request.get('shelter_email_donations'),
                            site_title=self.request.get('site_title'),
                            site_footer=self.request.get('site_footer'),
                            site_news=self.request.get('site_news'),
                            site_about_us_mission=self.request.get('site_about_us_mission'),
                            site_about_us_who=self.request.get('site_about_us_who'),
                            site_contact_us_emails=self.request.get('site_contact_us_emails'),
                            shelter_facebook=self.request.get('shelter_facebook'),
                            shelter_twitter=self.request.get('shelter_twitter'))

        shelter.put()
        CacheUtil.setCachedContent('shelter', shelter)
        self.redirect('/admin/')

def main():
    logging.getLogger().setLevel(logging.DEBUG)

    application = webapp.WSGIApplication([('/admin/?', MainHandler),
                                         ('/admin/shelter', ShelterSetupHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

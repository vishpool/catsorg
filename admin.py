#!/usr/bin/env python
#
import os
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        shelters = db.GqlQuery("SELECT * FROM Shelter ORDER BY date DESC LIMIT 10")
        shelter = shelters.get()

        if shelter:
            template_values = {
                'admin': user.nickname(),
                'shelter_admin': shelter.shelter_admin.nickname() + ' at ' + shelter.date.isoformat(),
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
        # shelter info

class Shelter(db.Model):
    active = db.BooleanProperty()
    shelter_id = db.StringProperty()
    shelter_admin = db.UserProperty()
    site_title = db.StringProperty()
    site_footer = db.StringProperty()
    api_key = db.StringProperty()
    api_secret = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class ShelterHandler(webapp.RequestHandler):
    def post(self):
        shelter = Shelter(active=True);
        shelter.shelter_id = self.request.get('shelter_id')
        shelter.site_title = self.request.get('site_title')
        shelter.site_footer = self.request.get('site_footer')
        shelter.api_key = self.request.get('api_key')
        shelter.api_secret = self.request.get('api_secret')

        if users.get_current_user():
            shelter.shelter_admin = users.get_current_user()

        shelter.put()
        self.redirect('/admin/')

def main():
    application = webapp.WSGIApplication([('/admin/', MainHandler),
                                         ('/admin/shelter', ShelterHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

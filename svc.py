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
    
    def get(self, req, name, animal_, animal, offset_, offset, format):

        if offset is None:
            offset = 0

        shelter = CacheUtil.getCachedContent('shelter')
        if shelter is None:
            shelter = Shelter.get_by_key_name('shelter')
            CacheUtil.setCachedContent('shelter', shelter)

        api = PetFinderAPI()
        pets = api.getShelterPets(offset, 12)

        if format == 'json': 
            res = {'svc': { name: pets }}
    
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(res))
        else:
            values = {'pets': pets}
 
            path = os.path.join(os.path.dirname(__file__), 'svc_' + name + '.html')
            self.response.out.write(template.render(path, values))
    

def main():

    logging.getLogger().setLevel(logging.DEBUG)

    application = webapp.WSGIApplication([('/svc/((adoptions)'
                                            '(/(barnyard|bird|cat|dog|horse|pig|reptile|smallfurry))?'
                                            '(/([0-9]+))?.(json|html))?', MainHandler)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

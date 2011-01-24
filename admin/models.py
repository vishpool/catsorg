from google.appengine.ext import db

class Shelter(db.Model):
    shelter_id = db.StringProperty(required=True)
    shelter_admin = db.UserProperty(required=True)
    site_title = db.StringProperty(required=True)
    site_footer = db.StringProperty(required=True)
    api_key = db.StringProperty(required=True)
    api_secret = db.StringProperty(required=True)
    updated = db.DateTimeProperty(auto_now_add=True)


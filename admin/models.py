from google.appengine.ext import db

class Shelter(db.Model):
    shelter_id = db.StringProperty(required=True)
    shelter_admin = db.UserProperty(required=True)
    api_key = db.StringProperty(required=True)
    api_secret = db.StringProperty(required=True)
    shelter_name = db.StringProperty(required=True)
    shelter_phone = db.PhoneNumberProperty(required=True)
    shelter_address = db.PostalAddressProperty(required=True)
    site_title = db.StringProperty(required=True)
    site_footer = db.StringProperty(required=True)
    site_news = db.TextProperty(required=True)
    site_about_us_mission = db.TextProperty(required=True)
    site_about_us_who = db.TextProperty(required=True)
    updated = db.DateTimeProperty(auto_now_add=True)


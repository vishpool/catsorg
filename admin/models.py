from google.appengine.ext import db
import pickle

class Shelter(db.Model):
    shelter_id = db.StringProperty(required=True)
    shelter_admin = db.UserProperty(required=True)
    api_key = db.StringProperty(required=True)
    api_secret = db.StringProperty(required=True)
    shelter_name = db.StringProperty(required=True)
    shelter_phone = db.PhoneNumberProperty(required=True)
    shelter_email = db.StringProperty(required=True)
    shelter_email_donations = db.StringProperty(required=False)
    shelter_address = db.PostalAddressProperty(required=True)
    site_title = db.StringProperty(required=True)
    site_footer = db.StringProperty(required=False)
    site_news = db.TextProperty(required=False)
    site_about_us_mission = db.TextProperty(required=True)
    site_about_us_who = db.TextProperty(required=True)
    site_contact_us_emails = db.TextProperty(required=False)
    shelter_facebook = db.StringProperty(required=False)
    shelter_twitter = db.StringProperty(required=False)
    google_analytics = db.StringProperty(required=False)
    updated = db.DateTimeProperty(auto_now_add=True)

class DictProperty(db.Property): 
    data_type = dict 
    
    def get_value_for_datastore(self, model_instance): 
        value = super(DictProperty, self).get_value_for_datastore(model_instance) 

        return db.Blob(pickle.dumps(value)) 
    
    def make_value_from_datastore(self, value): 
        if value is None: 
            return dict() 
        return pickle.loads(value) 
    
    def default_value(self): 
        if self.default is None: 
            return dict() 
        else: 
            return super(DictProperty, self).default_value().copy() 
    
    def validate(self, value): 
        if not isinstance(value, dict): 
            raise db.BadValueError('Property %s needs to be convertible ' 
                'to a dict instance (%s) of class dict' % (self.name, value)) 
                
        return super(DictProperty, self).validate(value) 
    
    def empty(self, value): 
        return value is None 

class Pet(db.Model):
    pet_id = db.StringProperty(required=True)
    pet_data = DictProperty(required=True)
    updated = db.DateTimeProperty(auto_now_add=True)


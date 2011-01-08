from google.appengine.ext import db


class OdeskApplication(db.Model):
    created = db.DateTimeProperty()
    updated = db.DateTimeProperty()
    secret_key = db.StringProperty()
    public_key = db.StringProperty()

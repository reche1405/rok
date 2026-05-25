from models import db 
import os
BASE_URL = "/media"
class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    relative_path = db.Column(db.String(255), nullable=False)
    alt_tag = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return self.title   

    def upload_to():
        return "media"
    
    def get_absolute_url(self):
        return BASE_URL + '/' + self.relative_path
    
    
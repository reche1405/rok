from promo.models import db 
from sqlalchemy import event
from flask import current_app
import os
BASE_URL = "/media"
class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    relative_path = db.Column(db.String(255), nullable=False)
    alt_tag = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return self.title   

    def upload_to():
        return "media"
    
    def get_absolute_url(self):
        return BASE_URL + '/' + self.relative_path
    
    def to_carousel_dict(self):
        """Convert media to carousel-friendly dictionary"""
        return {
            'id': self.id,
            'url': self.get_absolute_url(),
            'title': self.title,
            'description': self.description or '',
        }
    
@event.listens_for(Media, 'after_delete')
def delete_media_file(mapper, connection, target):
    """Delete the physical file when the database record is deleted"""
    if target.relative_path:
        relative_path = os.path.join(current_app.config['UPLOAD_PATH'], target.relative_path)
        try:
            if os.path.exists(relative_path):
                os.remove(relative_path)
                print(f"Deleted file: {relative_path}")
        except Exception as e:
            print(f"Failed to delete file {relative_path}: {e}")
        
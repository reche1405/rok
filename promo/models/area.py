from models import db

class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_desc = db.Column(db.String(500), nullable=False)
    featured_media_id = db.Column(db.Integer,  db.ForeignKey('media.id'), nullable=True)
    featured_media = db.relationship('Media', backref=db.backref('featured_area_images', lazy=True))
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_home(cls):
        return cls.query.limit(4).all()

    def __repr__(self):
        return self.title

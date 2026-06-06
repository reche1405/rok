from . import db
from .area import Area


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    area = db.relationship('Area', backref=db.backref('locations', lazy=True))
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.String(512), nullable=True)
    long_description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(255), nullable=True)
    def __repr__(self):
        return f'<Location {self.title}>'
    
    @classmethod
    def get_by_slug(cls, slug):
        """Returns a project by its slug."""
        return cls.query.filter_by(slug=slug).first()
    @classmethod
    def get_all(cls):
        return cls.query.all()
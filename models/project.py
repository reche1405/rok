from datetime import datetime
from models import db

project_services = db.Table('project_services',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)

project_media = db.Table('project_media',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'), primary_key=True)
)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(150), nullable=False)  
    desc = db.Column(db.Text, nullable=True) 
    short_desc = db.Column(db.String(500), nullable=False)
    featured = db.Column(db.Boolean, nullable=False)  
    slug = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=True)
    meta_id = db.Column(db.Integer, db.ForeignKey("metas.id"), nullable=True, unique=True)
    meta_obj = db.relationship("Meta", backref=db.backref("project", uselist=False), uselist=False)

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    location = db.relationship('Location', backref=db.backref('projects', lazy=True))

    services = db.relationship(
        'Service', 
        secondary=project_services, 
        backref=db.backref('projects', lazy='dynamic'),
        lazy='subquery'
    )
    media = db.relationship(
        'Media',
        secondary=project_media,
        backref=db.backref('projects', lazy='dynamic'),
        lazy='subquery'
    )
    featured_media_id = db.Column(db.Integer,  db.ForeignKey('media.id'), nullable=True)
    featured_media = db.relationship('Media', backref=db.backref('featured_project_images', lazy=True))

    def __repr__(self):
        return self.title

    @classmethod
    def get_featured(cls):
        """Returns only projects marked as featured."""
        return cls.query.filter_by(featured=True).all()

    @classmethod
    def get_all(cls):
        """Returns all projects."""
        return cls.query.all()

    @classmethod
    def get_by_slug(cls, slug):
        """Returns a project by its slug."""
        return cls.query.filter_by(slug=slug).first()
    

unit_media = db.Table('unit_media',
    db.Column('unit_id', db.Integer, db.ForeignKey('units.id'), primary_key=True),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'), primary_key=True)
)


class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('units', lazy=True))
    description = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    featured_media_id = db.Column(db.Integer,  db.ForeignKey('media.id'), nullable=True)
    featured_media = db.relationship('Media', backref=db.backref('featured_unit_images', lazy=True))

    media = db.relationship(
        'Media',
        secondary=unit_media,
        backref=db.backref('units', lazy='dynamic'),
        lazy='subquery'
    )



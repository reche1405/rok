from datetime import datetime
import enum
from promo.models import db
from sqlalchemy.ext.orderinglist import ordering_list

project_services = db.Table('project_services',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)


class ProjectTag(enum.Enum):
    LRG = 'Large Scale'
    KNB = 'Kitchens & Bathrooms'
    EXT = 'Extensions'

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
    tag = db.Column(db.Enum(ProjectTag), default=ProjectTag.LRG, nullable=False )
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    location = db.relationship('Location', backref=db.backref('projects', lazy=True))

    services = db.relationship(
        'Service', 
        secondary=project_services, 
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
    
    @classmethod
    def get_page(cls, page, items_per_page):
        if page is None or page < 1:
            page = 1
        if items_per_page is None or items_per_page < 1:
            items_per_page = 10
        offset = (page - 1) * items_per_page
        return cls.query.order_by(cls.id).offset(offset).limit(items_per_page).all()
    
    @classmethod
    def count(cls):
        return cls.query.count()
    
    def to_carousel_json(self):
        """Convert project media to carousel JSON format"""
        if not self.media: return

        return {
            'items': [media.to_carousel_dict() for media in self.media],
            'project_id': self.id,
            'project_title': self.title,
            'autoplay_interval': 4000  # or get from project settings
        }
    
    



class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('units', lazy=True))
    slug = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    featured_media_id = db.Column(db.Integer,  db.ForeignKey('media.id'), nullable=True)
    featured_media = db.relationship('Media', backref=db.backref('featured_unit_images', lazy=True))

    def __repr__(self):
        return self.title


    def to_carousel_json(self):
        """Convert project media to carousel JSON format"""
        if not self.media: return
        return {
            'items': [media.to_carousel_dict() for media in self.media],
            'project_id': self.id,
            'project_title': self.title,
            'autoplay_interval': 4000  # or get from project settings
        }

    @classmethod
    def get_by_slug(cls, slug):
        """Returns a project by its slug."""
        return cls.query.filter_by(slug=slug).first()


class Orientation(enum.Enum):
    Portrait = "portrait"
    Landscape = 'landscape'
    def __str__(self):
        return self.value

class Gallery(db.Model):
    __tablename__ = 'galleries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='Default Slideshow')
    orientation = db.Column(db.Enum(Orientation), default=Orientation.Portrait, nullable=False)
    
    # Foreign Key & Relationship to Project
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete="CASCADE"), unique=True, nullable=True)
    project = db.relationship('Project', backref=db.backref('gallery', uselist=False, lazy=True))

    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', ondelete="CASCADE"), unique=True, nullable=True)
    unit = db.relationship('Unit', backref=db.backref('gallery', uselist=False, lazy=True))

    slides = db.relationship(
        'Slide', 
        order_by='Slide.sort_order', 
        collection_class=ordering_list('sort_order'),
        cascade="all, delete-orphan",
        backref='gallery'
    )

    def __repr__(self):
        return f"<Gallery {self.name} (Project ID: {self.project_id})>"
    
    def to_json(self):
        return {
            "items" : [slide.to_json() for slide in self.slides],
            'orientation' : self.orientation.value,
            'project_id': self.project_id,
            'project_title': self.name,
            'autoplay_interval': 4000  # or get from project settings
            }

class Slide(db.Model):
    __tablename__ = 'slides'
    
    id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.id', ondelete="CASCADE"), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0) # Made non-nullable for ordering_list
    
    # Relationship to Media
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=False)
    # Changed backref to 'slides' (plural) to avoid naming collisions if Media is used elsewhere
    media = db.relationship('Media', backref=db.backref('slides', lazy=True))
    
    def __repr__(self):
        return f"<Slide id={self.id} gallery_id={self.gallery_id} order={self.sort_order}>"
    
    def to_json(self):
        return self.media.to_carousel_dict()


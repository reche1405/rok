from promo.models import db

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False )
    short_desc = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    svg = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(255), nullable=False)
    benefits_list_id = db.Column(db.Integer, db.ForeignKey('lisits.id'), nullable=True)
    benefits_list = db.relationship('List', backref=db.backref('service', uselist=False))
    featured_media_id = db.Column(db.Integer,  db.ForeignKey('media.id'), nullable=True)
    featured_media = db.relationship('Media', backref=db.backref('featured_service_images', lazy=True))
    def __repr__(self):
        return self.title

    @classmethod
    def get_home(cls):
        return cls.query.limit(4).all()
    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def get_by_slug(cls, slug):
        
        return cls.query.filter_by(slug=slug).first()


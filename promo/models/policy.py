from promo.models import db

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    nav_title = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), unique=True, nullable=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title
    
    @classmethod
    def get_by_slug(cls, slug):
        return cls.query.filter_by(slug=slug).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
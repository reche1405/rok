from models import db 
import os
class Meta(db.Model):
    __tablename__ = "metas"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    keywords = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title   

class Page(db.Model):
    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.Text, nullable=True)
    meta_id = db.Column(db.Integer, db.ForeignKey("metas.id"), nullable=False, unique=True)
    meta = db.relationship("Meta", backref=db.backref("page", uselist=False), uselist=False)
    tag = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return self.title   
    
    @classmethod
    def get_by_tag(cls, tag):
        if tag is None:
            return None
        return cls.query.filter(db.func.lower(cls.tag) == tag.lower()).first()
    
    

from models import db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

class List(db.Model):
    __tablename__ = "lisits"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    items = db.relationship('ListItem', backref='list', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return self.tag

    @classmethod
    def get_for_tag(cls, tag):
        try:
            return cls.query.filter_by(tag=tag).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return cls.query.filter_by(tag=tag).first()
        
    @classmethod
    def get_for_tags(cls, tags):
        tag_list = cls.query.filter(cls.tag.in_(tags)).all()
        return {x.tag: x for x in tag_list}

    @classmethod
    def get_home(cls):
        tags = ['why-rok', 'home-hero']
        tag_list = cls.query.filter(cls.tag.in_(tags)).all()
        return {x.tag: x for x in tag_list}


class ListItem(db.Model):
    __tablename__ = 'listitems'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    subtext = db.Column(db.Text, nullable=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lisits.id'), nullable=False)

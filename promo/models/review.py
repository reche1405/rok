from promo.models import db

class Review(db.Model):
    __tablename__="reviews"
id = db.Column(db.Integer, primary_key=True)
rating = db.Column(db.Integer, nullable=False)
project_id = db.Column(db.Integer, db.ForignKey('projects.id'), nullable=True)
project = db.relationship('Project', backref=db.backref('projects', lazy=True))
name = db.Column(db.String(255), nullable=True)
text = db.Column(db.Text, nullable=False)
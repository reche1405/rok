from models import db

class Social(db.Model):
    __tablename__ = "socials"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    page_uri = db.Column(db.String(255), nullable=False)
    handle = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"@{self.handle} on {self.title}"
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    

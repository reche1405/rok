from models import db
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
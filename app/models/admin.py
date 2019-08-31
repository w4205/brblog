from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Text
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import Base


class Admin(Base, UserMixin):
    id =Column(Integer, primary_key=True)
    username = Column(String(20))
    password_hash = Column(String(128))
    blog_title = Column(String(60))
    blog_sub_title = Column(String(100))
    name = Column(String(30))
    about = Column(Text)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def validate_password(self, hash):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, hash)
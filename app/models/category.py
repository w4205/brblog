from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from app.models import Base, db


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    posts = relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        self.status = 0
        db.session.commit()
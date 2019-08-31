from sqlalchemy import ForeignKey, Integer, Column, Boolean, Text, String
from sqlalchemy.orm import relationship

from app.models import Base, db


class Post(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    body = Column(Text, nullable=False)
    can_comment = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship('Category', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

    # 删除 post 时对应 comments 一并做删除标记
    def delete(self):
        comments = self.comments[:]
        for comment in comments:
            comment.status = 0
        self.status = 0
        db.session.commit()
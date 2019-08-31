from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models import  Base


class Comment(Base):
    id = Column(Integer, primary_key=True)
    author = Column(String(20), nullable=False)
    site = Column(String(256))
    email = Column(String(256), nullable=False)
    body = Column(Text, nullable=False)
    from_admin = Column(Boolean, default=False, nullable=False)
    reviewed = Column(Boolean, default=False, nullable=False)
    # 外键
    post_id = Column(Integer, ForeignKey('post.id'))
    replied_id = Column(Integer, ForeignKey('comment.id'))
    # 关系
    post = relationship('Post', back_populates='comments')
    replies = relationship('Comment', back_populates='replied',
                           cascade='all, delete-orphan')
    replied = relationship('Comment', back_populates='replies',
                           remote_side=[id])

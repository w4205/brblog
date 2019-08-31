from sqlalchemy import Column, Integer, String

from app.models import Base


class Link(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    url = Column(String(255))
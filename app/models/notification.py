from ..database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, func


class User(Base):
    __tablename__ = "notification"

    id = Column(String(255), primary_key=True)
    username = Column(String(42), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    password = Column(String(255))
    avatar = Column(String(255))
   

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, func
from ..database import Base


class Service(Base):
    __tablename__ = "service"

    id = Column(String(255), primary_key=True)
    name = Column(String(42), nullable=False, index=True)
    desc = Column(String(255))
    room = Column(String(255), nullable=False, index=True)
    avatar = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

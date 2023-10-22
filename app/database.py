from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text,
    func,
    ForeignKey,
    Boolean,
    DateTime,
    TEXT,
)
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://admin:admin@localhost:5432/DoAn_Apartment"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
    finally:
        db.close()


class User(Base):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True)
    username = Column(String(42), nullable=False, index=True)
    phonenumber = Column(String(42), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    password = Column(String(255))
    avatar = Column(String(255))
    isVerify = Column(Boolean, default=False)
    verification_code = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

    user_contract = relationship("Contract", back_populates="user")
    user_bill = relationship("Bill", back_populates="user")


class Contract(Base):
    __tablename__ = "contract"

    id = Column(String(255), primary_key=True)
    content = Column(TEXT)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))

    apartment_id = Column(
        String(255), ForeignKey("apartment.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    apartment = relationship("Apartment", back_populates="apartment_contract")
    user = relationship("User", back_populates="user_contract")


class Apartment(Base):
    __tablename__ = "apartment"

    id = Column(String(255), primary_key=True)
    name = Column(String(42), nullable=False, index=True)
    desc = Column(String(255))
    room = Column(String(255), nullable=False, index=True, unique=True)
    img_room = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

    # Tạo mối quan hệ với bảng User
    apartment_contract = relationship("Contract", back_populates="apartment")


class Bill(Base):
    __tablename__ = "bill"

    id = Column(String(255), primary_key=True)
    price = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

    service_id = Column(
        String(255), ForeignKey("service.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="user_bill")
    service = relationship("Service", back_populates="service_bill")


class Service(Base):
    __tablename__ = "service"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    desc = Column(String(255), nullable=False)
    service_type = Column(String(255))
    priority = Column(String(255))

    service_bill = relationship("Bill", back_populates="service")


class Notification(Base):
    __tablename__ = "notification"

    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"))
    send_all = Column(Boolean, default=False)
    title = Column(String(255), nullable=False)
    notification_type = Column(String(255), nullable=False, default="")
    desc = Column(TEXT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

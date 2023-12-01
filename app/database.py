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
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from enum import Enum

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


class UserRole(Enum):
    RENTER = "RENTER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True)
    username = Column(String(42), nullable=False, index=True)
    phonenumber = Column(String(42), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    password = Column(String(255))
    avatar = Column(String(255))
    isVerify = Column(Boolean, default=False)
    address = Column(String(255))
    verification_code = Column(String(255), unique=True)
    system_role = Column(String(52))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

    apartments = relationship("Apartment", back_populates="owner")
    user_contract = relationship("Contract", back_populates="user")
    user_bill = relationship("Bill", back_populates="user")
    messages = relationship("Message", back_populates="user")
    rooms = relationship("MembersRoom", back_populates="user")


class Contract(Base):
    __tablename__ = "contract"

    id = Column(String(255), primary_key=True)
    content = Column(TEXT)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))
    total_amount = Column(Integer, nullable=False, default=0)
    num_of_people = Column(Integer, nullable=False, default=0)
    status = Column(String(42), index=True, default="pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    apartment_id = Column(String(255), ForeignKey("apartment.id", ondelete="CASCADE"))
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"))

    apartment = relationship("Apartment", back_populates="apartment_contract")
    user = relationship("User", back_populates="user_contract")


apartment_amenity = Table(
    "apartment_amenity",
    Base.metadata,
    Column("apartment_id", String(255), ForeignKey("apartment.id")),
    Column("amenity_id", String(255), ForeignKey("amenity.id")),
)


class Apartment(Base):
    __tablename__ = "apartment"

    id = Column(String(255), primary_key=True)
    name = Column(String(42), nullable=False, index=True)
    desc = Column(TEXT)
    address = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )
    city = Column(String(255))
    apartment_type = Column(String(255))
    price_per_day = Column(Integer, nullable=False)
    num_bedrooms = Column(Integer, nullable=False)
    num_living_rooms = Column(Integer, nullable=False)
    num_bathrooms = Column(Integer, nullable=False)
    total_people = Column(Integer, nullable=False)
    is_approved = Column(Boolean, nullable=True, default=False)

    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"))

    # Tạo mối quan hệ với bảng User
    owner = relationship("User", back_populates="apartments")
    apartment_contract = relationship("Contract", back_populates="apartment")
    apartment_tags = relationship("ApartmentTag", back_populates="apartment")
    amenities = relationship(
        "Amenity", secondary=apartment_amenity, back_populates="apartments"
    )
    images = relationship("ApartmentImage", back_populates="apartment")
    comments = relationship("ApartmentComment", back_populates="apartment")


class ApartmentComment(Base):
    __tablename__ = "apartment_comment"

    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"))
    apartment_id = Column(String(255), ForeignKey("apartment.id", ondelete="CASCADE"))
    text = Column(TEXT)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    rate_location = Column(Integer, nullable=False)
    rate_amenities = Column(Integer, nullable=False)
    rate_interior = Column(Integer, nullable=False)
    rate_price = Column(Integer, nullable=False)

    user = relationship("User")  # replace 'User' with the actual User class
    apartment = relationship("Apartment", back_populates="comments")


class ApartmentImage(Base):
    __tablename__ = "apartment_image"
    id = Column(String(255), primary_key=True)
    apartment_id = Column(String(255), ForeignKey("apartment.id", ondelete="CASCADE"))
    image_url = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    apartment = relationship("Apartment", back_populates="images")


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


class ApartmentTag(Base):
    __tablename__ = "apartment_tag"

    id = Column(String(255), primary_key=True)
    apartment_id = Column(String(255), ForeignKey("apartment.id", ondelete="CASCADE"))
    tag_id = Column(String(255), ForeignKey("tag.id", ondelete="CASCADE"))

    tag = relationship("Tag", back_populates="tag_apartment")
    apartment = relationship("Apartment", back_populates="apartment_tags")


# Với mối quan hệ này, bạn có thể dễ dàng truy cập danh sách các tags của một apartment và danh sách các apartments của một tag thông qua các thuộc tính tags và apartments.


class Tag(Base):
    __tablename__ = "tag"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    desc = Column(String(255), nullable=False)
    tag_apartment = relationship("ApartmentTag", back_populates="tag")


# Lớp đại diện cho các tiện nghi
class Amenity(Base):
    __tablename__ = "amenity"

    id = Column(String(255), primary_key=True)
    name = Column(String(42), nullable=False, index=True)
    desc = Column(String(255), nullable=False)
    apartments = relationship(
        "Apartment", secondary=apartment_amenity, back_populates="amenities"
    )


class Message(Base):
    __tablename__ = "message"

    id = Column(String(255), primary_key=True)
    sender_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"))
    room_id = Column(String(255), ForeignKey("room.id", ondelete="CASCADE"))
    content = Column(TEXT)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

    room = relationship("Room", back_populates="messages")
    user = relationship("User", back_populates="messages")


class MembersRoom(Base):
    __tablename__ = "members_room"

    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"))
    room_id = Column(String(255), ForeignKey("room.id", ondelete="CASCADE"))

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

    room = relationship("Room", back_populates="members")
    user = relationship("User", back_populates="rooms")


class Room(Base):
    __tablename__ = "room"

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    key = Column(String(255))

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=func.current_timestamp(),
    )

    messages = relationship("Message", back_populates="room")
    members = relationship("MembersRoom", back_populates="room")

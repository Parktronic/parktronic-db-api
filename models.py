from sqlalchemy import Text, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from database import Base


class ParkingLot(Base):
    __tablename__ = "parking_lots"

    id = Column(Integer, primary_key=True)
    coordinates = Column(Text)  # Заменить на массив
    description = Column(Text)
    city = Column(String)
    street = Column(String)
    house = Column(Integer)

    views = relationship("View", back_populates="parking_lot")
    favorites = relationship("Favorite", back_populates="parking_lot")


class View(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True)
    parking_lot_id = Column(Integer, ForeignKey("parking_lots.id", ondelete="CASCADE"))
    camera = Column(Integer)

    parking_lot = relationship("ParkingLot", back_populates="views")
    rows = relationship("Row", back_populates="view")


class Row(Base):
    __tablename__ = "rows"

    id = Column(Integer, primary_key=True)
    view_id = Column(Integer, ForeignKey("views.id", ondelete="CASCADE"))
    coordinates = Column(Text)
    capacity = Column(Integer)
    free_places = Column(Text)
    last_updated = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    view = relationship("View", back_populates="rows")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    favorites = relationship("Favorite", back_populates="user")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    parking_lot_id = Column(Integer, ForeignKey("parking_lots.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="favorites")
    parking_lot = relationship("ParkingLot", back_populates="favorites")

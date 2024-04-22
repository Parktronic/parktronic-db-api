from sqlalchemy import Text, Column, ForeignKey, Integer, String, TIMESTAMP, text, ARRAY, Float
from sqlalchemy.orm import relationship

from database import Base


class ParkingLot(Base):
    __tablename__ = "parking_lots"

    id = Column(Integer, primary_key=True)
    coordinates = Column(ARRAY(Float), nullable=False)
    description = Column(Text)
    city = Column(String)
    street = Column(String)
    house = Column(Integer)

    views = relationship("View", back_populates="parking_lot")
    favorites = relationship("Favorite", back_populates="parking_lot")


class View(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True)
    parking_lot_id = Column(Integer, ForeignKey("parking_lots.id", ondelete="CASCADE"), nullable=False)
    camera = Column(Integer, nullable=False)

    parking_lot = relationship("ParkingLot", back_populates="views")
    rows = relationship("Row", back_populates="view")


class Row(Base):
    __tablename__ = "rows"

    id = Column(Integer, primary_key=True)
    view_id = Column(Integer, ForeignKey("views.id", ondelete="CASCADE"), nullable=False)
    coordinate_1 = Column(ARRAY(Float), nullable=False)
    coordinate_2 = Column(ARRAY(Float), nullable=False)
    coordinate_3 = Column(ARRAY(Float), nullable=False)
    capacity = Column(Integer, nullable=False)
    free_places = Column(ARRAY(Integer), nullable=False)
    last_updated = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parking_lot_id = Column(Integer, ForeignKey("parking_lots.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="favorites")
    parking_lot = relationship("ParkingLot", back_populates="favorites")


class PredictionInfo(Base):
    __tablename__ = "prediction_info"

    id = Column(Integer, primary_key=True)

    time = Column(String, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    weekday = Column(String, nullable=False)

    weather = Column(String, nullable=False)
    temperature = Column(Integer, nullable=False)
    wind = Column(Float, nullable=False)

    id_parking = Column(Integer,
                        ForeignKey("parking_lots.id", ondelete="CASCADE"),
                        nullable=False)
    coords = Column(ARRAY(Float), nullable=False)
    count_lots = Column(Integer, nullable=False)
    free_places = Column(Integer, nullable=False)

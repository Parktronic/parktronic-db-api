from typing import List, Optional
from pydantic import BaseModel


class ParkingLot(BaseModel):
    id: Optional[int]
    coordinates: str  # Заменить на массив
    description: str
    city: str
    street: str
    house: str


class View(BaseModel):
    camera: int


class Row(BaseModel):
    coordinates: str  # Заменить на массив
    capacity: int
    free_places: List[int]


class Rows(BaseModel):
    rows: List[Row]


class ParkingInfo(ParkingLot, View, Rows):
    def parking_lot(self) -> ParkingLot:
        return ParkingLot(**self.dict())  # Устаревший метод

    def view(self) -> View:
        return View(**self.dict())

    def rows(self) -> Rows:
        return Rows(**self.dict())


class ParkingID(BaseModel):
    id: int


class User(BaseModel):
    email: str
    password: str


class UserSignup(User):
    first_name: str
    username: str


class ParkingLotID(BaseModel):
    parking_lot_id: int


class UserParkings(UserSignup):
    parkings: List[int]

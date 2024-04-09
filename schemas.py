from typing import List, Optional
from pydantic import BaseModel


class Row(BaseModel):
    coords: List[List[float]]
    capacity: int
    free_places: List[int]


class ParkingLotResponse(BaseModel):
    id: int
    coords: List[float]
    description: str
    # city: str
    # street: str
    # house: int
    address: str
    # camera: int
    rows: List[Row]


class ParkingLotRequest(BaseModel):
    id: Optional[int]
    coords: List[float]
    description: str
    city: str
    street: str
    house: int
    # address: str
    camera: int
    rows: List[Row]


class ParkingLots(BaseModel):
    parking_lots: List[ParkingLotResponse]


class UserPassword(BaseModel):
    password: str


class UserEmail(BaseModel):
    email: str


class UserNames(BaseModel):
    first_name: str
    username: str


class UserLogin(UserPassword, UserEmail):
    pass


class UserSignup(UserLogin, UserNames):
    pass


class User(UserEmail, UserNames):
    parking_lots: List[int]


class ID(BaseModel):
    id: int

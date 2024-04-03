import random
import string
from typing import List, Dict, Any
from fastapi import FastAPI, Request, Response, HTTPException
from models import ParkingInfo, ParkingID, User, UserSignup
from database import ParktronicDatabase
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware


database = ParktronicDatabase("parktronic",
                              "postgres",
                              "postgres",
                              "127.0.0.1",
                              "5432")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["Content-Type",
                    "Set-Cookie",
                    "Access-Control-Allow-Headers",
                    "Access-Control-Allow-Origin",
                    "Authorization"]
)
CORS_HEADER = "http://localhost:8080"


@app.post("/parking_lot")
def post_parking_lot(data: ParkingInfo) -> ParkingID:
    parking_lot_id = database.update_parking_lot(data.parking_lot())
    view_id = database.update_view(parking_lot_id, data.view())
    database.update_rows(view_id, data.rows)
    return ParkingID(id=parking_lot_id)


@app.get("/parking_lots")
def get_parking_lots() -> Dict[str, List[Dict[str, Any]]]:
    return database.select_parking_lots()


def random_cookie(length=10) -> str:
    characters = string.ascii_letters + string.digits
    cookie_value = ''.join(random.choice(characters) for i in range(length))
    return cookie_value


@app.post("/signup")
def post_signup(user: UserSignup, request: Request, response: Response):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    if database.select_user_by_email(user) != []:
        return {"message": "You're already registered"}

    database.insert_user(user)

    if "session_id" not in request.cookies:
        cookie = random_cookie()
        response.set_cookie(key="session_id",
                            value=cookie,
                            expires=2500,
                            httponly=True)

    return {"message": "Successfully registered"}


@app.post("/login")
def post_login(user: User, request: Request, response: Response):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    if database.select_user(user) == []:
        raise HTTPException(404, "User not found")

    if "session_id" not in request.cookies:
        cookie = random_cookie()
        response.set_cookie(key="session_id",
                            value=cookie,
                            expires=2500,
                            httponly=True)

    return {"message": "Successfully logged in"}

import random
import string
from typing import List, Dict, Any
from fastapi import FastAPI, Request, Response, HTTPException
from models import ParkingInfo, ParkingID, User, UserSignup, ParkingLotID
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
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"]
)
CORS_HEADER = "http://localhost:8080"
cookies = {}


@app.post("/parking_lot")
def post_parking_lot(data: ParkingInfo, response: Response) -> ParkingID:
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    parking_lot_id = database.update_parking_lot(data.parking_lot())
    view_id = database.update_view(parking_lot_id, data.view())
    database.update_rows(view_id, data.rows)
    return ParkingID(id=parking_lot_id)


@app.get("/parking_lots")
def get_parking_lots(response: Response) -> Dict[str, List[Dict[str, Any]]]:
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

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

    user_id = database.insert_user(user)

    if "session_id" not in request.cookies:
        cookie = random_cookie()
        response.set_cookie(key="session_id",
                            value=cookie,
                            expires=2500,
                            httponly=True)
        cookies[cookie] = user_id

    user = database.select_user_by_id(user_id)

    parkings = database.select_favorites(user_id)

    return UserSignup(email=user[1],
                      first_name=user[2],
                      username=user[3],
                      password=user[4],
                      parkings=parkings)


@app.post("/login")
def post_login(user: User, request: Request, response: Response):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    user_id = database.select_user(user)

    if user_id == []:
        raise HTTPException(404, "User not found")

    if "session_id" not in request.cookies:
        cookie = random_cookie()
        response.set_cookie(key="session_id",
                            value=cookie,
                            expires=2500,
                            httponly=True)
        cookies[cookie] = user_id

    user = database.select_user_by_id(user_id)

    parkings = database.select_favorites(user_id)

    return UserSignup(email=user[1],
                      first_name=user[2],
                      username=user[3],
                      password=user[4],
                      parkings=parkings)


@app.get("/is_authorized")
def get_is_authorized(request: Request, response: Response):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    if "session_id" not in request.cookies:
        raise HTTPException(401, "User not found")

    cookie = request.cookies["session_id"]

    user_id = cookies[cookie]

    user = database.select_user_by_id(user_id)

    parkings = database.select_favorites(user_id)

    return UserSignup(email=user[1],
                      first_name=user[2],
                      username=user[3],
                      password=user[4],
                      parkings=parkings)


@app.get("/logout")
def get_logout(request: Request, response: Response):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    if "session_id" not in request.cookies:
        raise HTTPException(401, "User not found")

    response.delete_cookie("session_id")

    cookie = request.cookies["session_id"]

    del cookies[cookie]

    return {"message": "Successfully logged out"}


@app.post("/favorite")
def post_favorite(parking_lot_id: ParkingLotID, request: Request, response: Response):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    if "session_id" not in request.cookies:
        raise HTTPException(401, "User not found")

    cookie = request.cookies["session_id"]

    user_id = cookies[cookie]

    result = database.insert_favorite(user_id, parking_lot_id.parking_lot_id)

    user = database.select_user_by_id(user_id)

    parkings = database.select_favorites(user_id)

    return UserSignup(email=user[1],
                      first_name=user[2],
                      username=user[3],
                      password=user[4],
                      parkings=parkings)

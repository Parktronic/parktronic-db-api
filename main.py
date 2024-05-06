import os
import random
import string
from typing import List, Dict, Any
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import ParkingLotRequest, ParkingLots, UserLogin, UserSignup, User, ID
from database import SessionLocal, engine
import crud, models, schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://79.174.91.217"],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"]
)
CORS_HEADER = "http://79.174.91.217"

cookies = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def random_cookie(length=10) -> str:
    characters = string.ascii_letters + string.digits
    cookie_value = ''.join(random.choice(characters) for i in range(length))
    return cookie_value


@app.get("/api/parking_lots", response_model=ParkingLots)
def get_parking_lots(response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    return crud.select_parking_lots(db)


@app.post("/api/parking_lot", response_model=ID)
def update_parking_lot(parking_lot: ParkingLotRequest, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    return crud.insert_or_update_parking_lot(db, parking_lot)


@app.post("/api/signup", response_model=User)
def sign_up(user: UserSignup, request: Request, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    if crud.select_user_by_email(db, user.email) is not None:
        raise HTTPException(409)

    user_id = crud.insert_user(db, user)

    if "session_id" in request.cookies:
        cookie_value = request.cookies["session_id"]
        if cookie_value in cookies.keys():
            del cookies[cookie_value]

    cookie = random_cookie()
    response.set_cookie(key="session_id",
                        value=cookie,
                        expires=2500,
                        httponly=True)
    cookies[cookie] = user_id

    user_db = crud.select_user_by_id(db, user_id)

    return {
        "email": user_db.email,
        "first_name": user_db.first_name,
        "username": user_db.username,
        "parking_lots": [favorite.parking_lot_id for favorite in user_db.favorites]
    }


@app.post("/api/login", response_model=User)
def log_in(user: UserLogin, request: Request, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    user_db = crud.select_user_by_email_and_password(db, user.email, user.password)

    if user_db is None:
        raise HTTPException(404)

    if "session_id" in request.cookies:
        cookie_value = request.cookies["session_id"]
        if cookie_value in cookies.keys():
            del cookies[cookie_value]

    cookie = random_cookie()
    response.set_cookie(key="session_id",
                        value=cookie,
                        expires=2500,
                        httponly=True)
    cookies[cookie] = user_db.id

    return {
        "email": user_db.email,
        "first_name": user_db.first_name,
        "username": user_db.username,
        "parking_lots": [favorite.parking_lot_id for favorite in user_db.favorites]
    }


@app.get("/api/is_authorized", response_model=User)
def is_user_authorized(request: Request, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    if "session_id" not in request.cookies or request.cookies["session_id"] not in cookies.keys():
        raise HTTPException(401)

    user_id = cookies[request.cookies["session_id"]]

    user_db = crud.select_user_by_id(db, user_id)

    return {
        "email": user_db.email,
        "first_name": user_db.first_name,
        "username": user_db.username,
        "parking_lots": [favorite.parking_lot_id for favorite in user_db.favorites]
    }


@app.post("/api/logout")
def log_out(request: Request, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    if "session_id" not in request.cookies or request.cookies["session_id"] not in cookies.keys():
        raise HTTPException(401)

    cookie_value = request.cookies["session_id"]
    if cookie_value in cookies.keys():
        del cookies[cookie_value]

    response.delete_cookie("session_id")


@app.post("/api/favorite", response_model=User)
def add_favorite_parking_lot(parking_lot_id: ID, request: Request, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    if "session_id" not in request.cookies or request.cookies["session_id"] not in cookies.keys():
        raise HTTPException(401)

    user_id = cookies[request.cookies["session_id"]]

    if crud.select_favorite(db, user_id, parking_lot_id.id) is not None:
        raise HTTPException(422)

    crud.insert_favorite(db, user_id, parking_lot_id.id)

    user_db = crud.select_user_by_id(db, user_id)

    return {
        "email": user_db.email,
        "first_name": user_db.first_name,
        "username": user_db.username,
        "parking_lots": [favorite.parking_lot_id for favorite in user_db.favorites]
    }


@app.delete("/api/favorite", response_model=User)
def delete_favorite(parking_lot_id: ID, request: Request, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    print(cookies)

    if "session_id" not in request.cookies or request.cookies["session_id"] not in cookies.keys():
        raise HTTPException(401)

    user_id = cookies[request.cookies["session_id"]]

    crud.delete_favorite(db, user_id, parking_lot_id.id)

    user_db = crud.select_user_by_id(db, user_id)

    return {
        "email": user_db.email,
        "first_name": user_db.first_name,
        "username": user_db.username,
        "parking_lots": [favorite.parking_lot_id for favorite in user_db.favorites]
    }

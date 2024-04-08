import random
import string
from typing import List, Dict, Any
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import ParkingLot, ParkingLots, UserLogin, UserSignup, User, ID
from database import SessionLocal, engine
import crud, models, schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/parking_lots", response_model=ParkingLots)
def get_parking_lots(response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    return crud.get_parking_lots(db)


@app.post("/parking_lot", response_model=ID)
def post_parking_lot(parking_lot: ParkingLot, response: Response, db: Session = Depends(get_db)):
    response.headers["Access-Control-Allow-Origin"] = CORS_HEADER

    return crud.update_parking_lot(db, parking_lot)

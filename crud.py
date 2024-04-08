from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas


def select_parking_lots(db: Session):
    result = []

    parking_lots = db.query(models.ParkingLot).all()

    for parking_lot in parking_lots:

        views = parking_lot.views
        for view in views:
            result_rows = []

            rows = view.rows
            for row in rows:
                result_rows.append({
                    "coordinates": [row.coordinate_1, row.coordinate_2, row.coordinate_3],
                    "capacity": row.capacity,
                    "free_places": row.free_places
                })

        result.append({
            "id": parking_lot.id,
            "coordinates": parking_lot.coordinates,
            "description": parking_lot.description,
            "city": parking_lot.city,
            "street": parking_lot.street,
            "house": parking_lot.house,
            "rows": result_rows
        })

    return {"parking_lots": result}


def insert_or_update_parking_lot(db: Session, parking_lot: schemas.ParkingLotRequest):
    try:
        if parking_lot.id is not None:
            db.query(models.View) \
              .filter_by(parking_lot_id=parking_lot.id, camera=parking_lot.camera) \
              .delete()
            parking_lot_db = db.query(models.ParkingLot) \
                               .filter_by(id=parking_lot.id) \
                               .first()
        else:
            parking_lot_db = models.ParkingLot()
            db.add(parking_lot_db)

        parking_lot_db.coordinates = parking_lot.coordinates
        parking_lot_db.description = parking_lot.description
        parking_lot_db.city = parking_lot.city
        parking_lot_db.street = parking_lot.street
        parking_lot_db.house = parking_lot.house

        db.flush()

        view = models.View()

        view.parking_lot_id=parking_lot_db.id,
        view.camera=parking_lot.camera

        db.add(view)
        db.flush()

        for row in parking_lot.rows:
            row = models.Row(view_id=view.id,
                             coordinate_1=row.coordinates[0],
                             coordinate_2=row.coordinates[1],
                             coordinate_3=row.coordinates[2],
                             capacity=row.capacity,
                             free_places=row.free_places,
                             last_updated=datetime.utcnow())
            db.add(row)
    except IntegrityError as error:
        db.rollback()
        raise error
    else:
        db.commit()
        return {"id": parking_lot_db.id}


def select_user_by_email(db: Session, email: str):
    user_db = db.query(models.User) \
                .filter_by(email=email) \
                .first()

    return user_db


def insert_user(db: Session, user: schemas.UserSignup):
    user_db = models.User(
        email=user.email,
        first_name=user.first_name,
        username=user.username,
        password=user.password
    )

    db.add(user_db)
    db.commit()

    return user_db.id


def select_user_by_id(db: Session, id: int):
    user_db = db.query(models.User) \
                .filter_by(id=id) \
                .first()

    return user_db


def select_user_by_email_and_password(db: Session, email: str, password: str):
    user_db = db.query(models.User) \
                .filter_by(email=email, password=password) \
                .first()

    return user_db


# def insert_parking_lot

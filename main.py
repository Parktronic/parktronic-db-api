from typing import List, Dict, Any
from fastapi import FastAPI
from models import ParkingInfo, ParkingID
from database import ParktronicDatabase


database = ParktronicDatabase("parktronic",
                              "postgres",
                              "postgres",
                              "127.0.0.1",
                              "5432")
app = FastAPI()


@app.post("/parking_lot")
def post_parking_lot(data: ParkingInfo) -> ParkingID:
    parking_lot_id = database.update_parking_lot(data.parking_lot())
    view_id = database.update_view(parking_lot_id, data.view())
    database.update_rows(view_id, data.rows)
    return ParkingID(id=parking_lot_id)


@app.get("/parking_lots")
def get_parking_lots() -> List[Dict[str, Any]]:
    return database.select_parking_lots()

from typing import List, Dict, Any
import json
import psycopg2
from models import ParkingLot, View, Rows


class PostgresConnector:
    def __init__(self, dbname, user, password, hostaddr, port):
        self.connection = psycopg2.connect(f"""
                                           dbname={dbname}
                                           user={user}
                                           password={password}
                                           hostaddr={hostaddr}
                                           port={port}
                                           """)

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()

    def __del__(self):
        self.connection.close()


class PostgresQueryExecutor:
    def __init__(self, dbname, user, password, hostaddr, port):
        self.connector = PostgresConnector(dbname,
                                           user,
                                           password,
                                           hostaddr,
                                           port)

    def execute(self, query):
        with self.connector as cursor:
            cursor.execute(query)
            try:
                result = cursor.fetchall()
            except psycopg2.ProgrammingError:
                result = None

        return result


class ParktronicDatabase:
    def __init__(self, dbname, user, password, hostaddr, port):
        self.query_executor = PostgresQueryExecutor(dbname,
                                                    user,
                                                    password,
                                                    hostaddr,
                                                    port)

    def select_parking_lots(self) -> List[Dict[str, Any]]:
        result = []
        parking_lots = self.query_executor.execute("""
                                                   select * from parking_lots;
                                                   """)
        for parking_lot in parking_lots:
            try:
                json.loads(parking_lot[1])
            except Exception:
                coordinates = []
            else:
                coordinates = json.loads(parking_lot[1])
            view_id = self.query_executor.execute(f"""
                                                  select id
                                                  from views
                                                  where parking_lot_id = {parking_lot[0]}
                                                  """)[0][0]  # Предполагаем, что один вид
            rows = self.query_executor.execute(f"""
                                               select coordinates, capacity, free_places
                                               from rows
                                               where view_id = {view_id}
                                               """)
            result_rows = []
            for row in rows:
                try:
                    json.loads(row[2])
                except:
                    free_places = []
                else:
                    free_places = json.loads(row[2])

                try:
                    json.loads(row[0])
                except Exception:
                    row_coordinates = []
                else:
                    row_coordinates = json.loads(row[0])

                result_rows.append({"coords": row_coordinates,
                                    "number": row[1],
                                    "free_spaces": free_places})

            result.append({"id": parking_lot[0],
                           "coords": coordinates, # Changed (was coordinates[0][0])
                           "description": parking_lot[2],
                           "address": parking_lot[3] + ', ' + parking_lot[4] + ', ' + str(parking_lot[5]),
                           "parking_rows": result_rows})

        return result

    def update_parking_lot(self, data: ParkingLot) -> int:
        if data.id is None:
            result = self.query_executor.execute(f"""
                                                 insert into parking_lots
                                                 (coordinates, description, city, street, house)
                                                 values ('{data.coordinates}',
                                                         '{data.description}',
                                                         '{data.city}',
                                                         '{data.street}',
                                                         '{data.house}')
                                                 returning id;
                                                 """)[0][0]
        else:
            result = self.query_executor.execute(f"""
                                                 update parking_lots
                                                 set coordinates = '{data.coordinates}',
                                                     description = '{data.description}',
                                                     city = '{data.city}',
                                                     street = '{data.street}',
                                                     house = '{data.house}'
                                                 where id = {data.id}
                                                 returning id;
                                                 """)[0][0]
        return result

    def update_view(self, parking_lot_id: int, data: View) -> int:
        self.query_executor.execute(f"""
                                    delete from views
                                    where parking_lot_id = {parking_lot_id}
                                    and camera = {data.camera};
                                    """)
        return self.query_executor.execute(f"""
                                           insert into views
                                           (parking_lot_id, camera)
                                           values ({parking_lot_id},
                                                   {data.camera})
                                           returning id;
                                           """)[0][0]

    def update_rows(self, view_id: int, data: Rows) -> None:
        self.query_executor.execute(f"""
                                    delete from rows
                                    where view_id = {view_id};
                                    """)
        for row in data:
            self.query_executor.execute(f"""
                                        insert into rows
                                        (view_id, coordinates, capacity, free_places)
                                        values ({view_id},
                                               '{row.coordinates}',
                                                {row.capacity},
                                               '{row.free_places}')
                                        """)

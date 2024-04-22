import json
import requests
import datetime
import pandas as pd
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


units = 'metric'
lang = 'ru'
appid = '0f258ef33a169309be54901c426dc9cd'


def get_weather_features(lat: float, lon: float) -> dict:
    '''
    Получает информацию о погоде по координатам.

    Args:
        lat (float): широта.
        lon (float): долгота.

    Returns:
        dict: словарь с информацией о погоде.
    '''
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&lang={lang}&appid={appid}'

    weather_data = requests.get(url).json()
    # weather_data_structure = json.dumps(weather_data, indent=2)
    # print(weather_data_structure)

    weather = weather_data['weather'][0]['main']
    temperature = round(weather_data['main']['temp'])
    wind = weather_data['wind']['speed']

    return {
        'weather': weather,
        'temperature': temperature,
        'wind': wind
    }


def get_features_from_detector() -> list:
    '''
    Получает необходимые фичи от детектора.

    Returns:
        list[dict]: список словарей с информацией от детектора вида:
        {"id_parking", "coords", "count_lots", "free_places"}
    '''
    db = SessionLocal()

    features = []

    # Идентификаторы всех парковок
    ids = crud.select_all_parkings_id(db)

    for parking_id in ids:
        parking_info = crud.select_parking_lots_by_id(db, parking_id)
        views = crud.select_all_views_by_parking_id(db, parking_id)
        for view in views:
            row = crud.select_last_row_info_by_view_id(db, view.id)
            feature = {
                "id_parking": parking_id,
                "coords": parking_info["coordinates"],
                "count_lots": row["capacity"],
                "free_places": len(row["free_places"])
            }
            features.append(feature)

    return features


def datetime_features() -> dict:
    '''
    Получает информацию о текущей дате, времени и дне недели.

    Returns:
        dict: словарь с информацией о текущей дате, времени и дне недели.
    '''
    now = datetime.datetime.now()

    # Извлекаем различные характеристики из текущей даты и времени
    time = f'{now.hour:02}:{now.minute:02}:{now.second:02}'
    day = now.day
    month = now.month
    weekday = now.strftime('%A')

    return {
        'time': time,
        'day': day,
        'month': month,
        'weekday': weekday
    }


def form_dataset():
    '''
    Формирует датасет с необходимой информацией.
    Целевая переменная - free_places.
    '''
    # Пустой список для хранения данных
    all_data = []

    # Получение данных
    detector_data = get_features_from_detector()

    # Для каждой парковки собираем данные
    for ddata in detector_data:
        lat, lon = ddata["coords"][0], ddata["coords"][1]

        weather_data = get_weather_features(lat, lon)
        datetime_data = datetime_features()

        # Объединение данных
        data = {**datetime_data, **weather_data, **ddata}

        all_data.append(data)

    # Преобразование в DataFrame
    df = pd.DataFrame(all_data)

    return df


def upload_dataframe_to_database(df, table_name="prediction_info") -> None:
    '''
    Загружает DataFrame в базу данных.
    '''
    df.to_sql(table_name, engine, if_exists='append', index=False)

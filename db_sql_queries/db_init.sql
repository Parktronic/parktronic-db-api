CREATE DATABASE parktronic;

CREATE TABLE parking_lots (
    id SERIAL PRIMARY KEY,
    coordinates VARCHAR,
    description TEXT,
    city VARCHAR,
    street VARCHAR,
    house INTEGER
);

CREATE TABLE views (
    id SERIAL PRIMARY KEY,
    parking_lot_id INTEGER REFERENCES parking_lots(id) ON DELETE CASCADE,
    camera INTEGER
);

CREATE TABLE rows (
    id SERIAL PRIMARY KEY,
    view_id INTEGER REFERENCES views(id) ON DELETE CASCADE,
    coordinates TEXT,
    capacity INTEGER,
    free_places TEXT,
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    parking_lot_id INTEGER REFERENCES parking_lots(id) ON DELETE CASCADE
);

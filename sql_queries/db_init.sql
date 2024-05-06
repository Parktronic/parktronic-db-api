CREATE DATABASE parktronic;

-- \c parktronic

-- CREATE TABLE parking_lots (
--     id SERIAL PRIMARY KEY,
--     coordinates TEXT NOT NULL,
--     description TEXT,
--     city VARCHAR,
--     street VARCHAR,
--     house INTEGER
-- );

-- CREATE TABLE views (
--     id SERIAL PRIMARY KEY,
--     parking_lot_id INTEGER REFERENCES parking_lots(id) ON DELETE CASCADE NOT NULL,
--     camera INTEGER NOT NULL
-- );

-- CREATE TABLE rows (
--     id SERIAL PRIMARY KEY,
--     view_id INTEGER REFERENCES views(id) ON DELETE CASCADE NOT NULL,
--     coordinates TEXT NOT NULL,
--     capacity INTEGER NOT NULL,
--     free_places TEXT NOT NULL,
--     last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR NOT NULL,
--     first_name VARCHAR NOT NULL,
--     username VARCHAR NOT NULL,
--     password VARCHAR NOT NULL
-- );

-- CREATE TABLE favorites (
--     id SERIAL PRIMARY KEY,
--     user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
--     parking_lot_id INTEGER REFERENCES parking_lots(id) ON DELETE CASCADE NOT NULL
-- );

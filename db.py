import os
import sqlite3

DB_FILEPATH = './weather.sqlite'

CREATE_LOCATION_TABLE = '''
    DROP TABLE IF EXISTS location;

    CREATE TABLE location (
        str TEXT    NOT NULL PRIMARY KEY,
        id  INTEGER NOT NULL
    );
'''

CREATE_WEATHER_TABLE = '''
    DROP TABLE IF EXISTS weather;

    CREATE TABLE weather (
        id                     INTEGER     NOT NULL PRIMARY KEY,
        location_id            INTEGER     NOT NULL,
        applicable_date        DATE        NOT NULL,
        created                DATETIME    NOT NULL,
        weather_state_name     TEXT        NOT NULL,
        weather_state_abbr     TEXT        NOT NULL,
        min_temp               FLOAT       NOT NULL,
        max_temp               FLOAT       NOT NULL,
        the_temp               FLOAT       NOT NULL,
        air_pressure           FLOAT       NOT NULL,
        humidity               INTEGER     NOT NULL,
        visibility             FLOAT,
        predictability         INTEGER     NOT NULL,
        wind_direction         FLOAT       NOT NULL,
        wind_direction_compass TEXT        NOT NULL,
        wind_speed             FLOAT       NOT NULL,

        FOREIGN KEY (location_id) REFERENCES location(id)
    );

    CREATE INDEX idx_weather_location_date ON weather(location_id, applicable_date);
'''

WEATHER_COLS = [
    'id', 'location_id', 'applicable_date', 'created', 'weather_state_name', 'weather_state_abbr',
    'min_temp', 'max_temp', 'the_temp', 'air_pressure', 'humidity', 'visibility', 'predictability',
    'wind_direction', 'wind_direction_compass', 'wind_speed'
]

def row_factory(conn, row):
    return dict([(col[0], row[i]) for i, col in enumerate(conn.description)])

def get_conn():
    conn = sqlite3.connect(DB_FILEPATH)
    conn.row_factory = row_factory
    return conn

def create_db():
    conn = get_conn()
    for script in [CREATE_LOCATION_TABLE, CREATE_WEATHER_TABLE]:
        conn.executescript(script)
    conn.commit()

def check_init_db(reset_db):
    if reset_db or not os.path.isfile(DB_FILEPATH):
        create_db()

def get_location_id(conn, location_str):
    stmt = 'SELECT id FROM location WHERE str = ?'
    row = conn.execute(stmt, (location_str,)).fetchone()
    if row is None:
        return None
    return row['id']

def save_location(conn, location_str, location_id):
    stmt = 'INSERT INTO location VALUES (?, ?)'
    conn.execute(stmt, (location_str, location_id))
    conn.commit()

def get_weather(conn, location_id, date):
    stmt = 'SELECT * FROM weather WHERE location_id = ? AND applicable_date = ? ORDER BY created'
    return list(conn.execute(stmt, (location_id, date)))

def save_weather(conn, weather):
    if not len(weather):
        return
    rows = [[row[col] for col in WEATHER_COLS] for row in weather]
    stmt = 'INSERT INTO weather ({}) VALUES ({})'.format(', '.join(WEATHER_COLS), ', '.join(['?' for col in WEATHER_COLS]))
    conn.executemany(stmt, rows)
    conn.commit()

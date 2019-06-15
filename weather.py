#!/usr/bin/env python3

import csv
import io
import sys

import api
import cli
import db
import errors as e

def main(location_str, date, reset_db):
    db.check_init_db(reset_db)

    try:
        weather = get_weather(location_str, date)
    except (e.LocationNotFoundError, e.NoWeatherDataFoundError) as err:
        print(err.description, file=sys.stderr)
        sys.exit(1)

    csv = get_weather_csv(weather)
    print(csv)

def get_weather(location_str, date):
    conn = db.get_conn()
    location_id = get_location_id(conn, location_str)
    return get_weather_data(conn, location_id, date)

def get_weather_csv(weather):
    output = io.StringIO()
    writer = csv.DictWriter(output, db.WEATHER_COLS, quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    writer.writerows(weather)
    return output.getvalue()

def get_location_id(conn, location_str):
    location_id = db.get_location_id(conn, location_str)
    if location_id is None:
        location_id = api.fetch_location_id(location_str)
        if location_id is None:
            raise e.LocationNotFoundError()
        db.save_location(conn, location_str, location_id)
    return location_id

def get_weather_data(conn, location_id, date):
    weather = db.get_weather(conn, location_id, date)
    if not len(weather):
        weather = api.fetch_weather_data(location_id, date)
        if not len(weather):
            raise e.NoWeatherDataFoundError()
        for row in weather:
            row['location_id'] = location_id
        db.save_weather(conn, weather)
    return weather

if __name__ == "__main__":
    args = cli.parse_args()
    main(args.location, args.date, args.reset_db)

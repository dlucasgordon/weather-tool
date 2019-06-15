# weather-tool
Simple tool to collect and display weather data from the [metaweather api](https://www.metaweather.com/api/).

Note that I would usually use click for the cli, sqlalchemy for db interaction, and arrow for date parsing, but we are trying to minimize the library requirements. The only external library requirement is the requests package.

To run, try:

    pip3 install requirements.txt
    python3 weather.py --help
    python3 weather.py
    python3 weather.py 'Los Angeles'
    python3 weather.py 'Los Angeles' 2019-1-1
    python3 weather.py 'Los Angeles' 2019-1-1 > la_weather_2019-1-1.csv

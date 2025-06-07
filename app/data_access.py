from .data_types import WeatherReport
from .errors import CityNotFoundError


db: dict[str, WeatherReport] = {}


def db_add_weather_report(city: str, report: WeatherReport) -> None:
    db[city] = report
    return db.get(city)


def db_get_weather_report(city: str) -> WeatherReport | None:
    try:
        return db[city]
    except KeyError:
        raise CityNotFoundError(f"City '{city}' not found in the database.")

def db_delete_weather_report(city: str) -> None:
    try:
        del db[city]
    except KeyError:
        raise CityNotFoundError(f"City '{city}' not found in the database.")
    return None


def db_update_weather_report(city: str, report: WeatherReport) -> WeatherReport | None:
    if city not in db:
        raise CityNotFoundError(f"City '{city}' not found in the database.")
    db[city] = report
    return db.get(city)
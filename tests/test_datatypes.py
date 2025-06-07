import pytest
from datetime import datetime, timezone
from app.data_types import WeatherReport, ConditionType
from pydantic import ValidationError

def test_weather_report_valid():
    report = WeatherReport(
        city="london",
        temperature=21.5,
        condition=ConditionType.SUNNY,
        timestamp=datetime(2025, 6, 7, 10, 0, tzinfo=timezone.utc)
    )
    assert report.city == "london"
    assert report.temperature == 21.5
    assert report.condition == ConditionType.SUNNY
    assert report.timestamp.year == 2025

@pytest.mark.parametrize(
    "city, temperature, condition",
    [
        (None, 20.0, ConditionType.SUNNY),          # City None
        ("london", None, ConditionType.SUNNY),      # Temp is none
        ("london", 20.0, None),                     # Weather condition None
        ("london", "hot", ConditionType.SUNNY),     # Wrong type for temperature
        ("london", 20.0, "WINDY"),                  # Invalid enum value
    ]
)
def test_weather_report_invalid(city, temperature, condition):
    with pytest.raises(ValidationError):
        WeatherReport(
            city=city,
            temperature=temperature,
            condition=condition,
            timestamp=datetime(2025, 6, 7, 10, 0, tzinfo=timezone.utc)
        )
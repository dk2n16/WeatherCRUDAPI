from datetime import datetime, timezone
import pytest

from app import create_app
from app import data_access
from app.data_types import WeatherReport, ConditionType


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def populated_db():
    data_access.db.clear()
    data_access.db.update({
        "london": WeatherReport(
            city="london",
            temperature=15.0,
            condition=ConditionType.CLOUDY,
            timestamp=datetime(2025, 6, 7, 10, 0, tzinfo=timezone.utc)
        ),
        "paris": WeatherReport(
            city="paris",
            temperature=22.0,
            condition=ConditionType.SUNNY,
            timestamp=datetime(2025, 6, 7, 11, 0, tzinfo=timezone.utc)
        ),
        "barcelona": WeatherReport(
            city="barcelona",
            temperature=28.0,
            condition=ConditionType.RAINY,
            timestamp=datetime(2025, 6, 7, 12, 0, tzinfo=timezone.utc)
        ),
    })

@pytest.fixture(autouse=True)
def clear_db():
    """Clear the database before and after each test."""
    data_access.db.clear()


@pytest.fixture
def test_post_update_data():
    return {
        "city": "london",
        "condition": "Sunny",
        "temperature": 20.0,
    }
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

class ConditionType(Enum):
    SUNNY = "Sunny"
    RAINY = "Rainy"
    CLOUDY = "Cloudy"
    SNOWY = "Snowy"
    FOGGY = "Foggy"


class WeatherReport(BaseModel):
    city: str = Field(..., description="The location of the weather report")
    temperature: float = Field(..., description="The temperature in degrees Celsius")
    condition: ConditionType = Field(..., description="The weather condition")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="The timestamp of the report creation/update")
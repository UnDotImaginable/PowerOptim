"""
Schemas for sensor reading data validation.
These define what data the Raspberry Pi must send to the backend.
"""
from pydantic import BaseModel
from typing import Optional


class SensorReadingCreate(BaseModel):
    """
    Data the Raspberry Pi sends with each reading.
    battery_level and power_source are required.
    voltage, current, temperature are optional.
    (for now)
    """
    battery_level: int
    power_source: str
    voltage: Optional[float] = None
    current: Optional[float] = None
    temperature: Optional[float] = None
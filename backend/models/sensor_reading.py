"""
SensorReading model for storing Raspberry Pi sensor data
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.database import Base


class SensorReading(Base):
    """
    A single snapshot of sensor data sent from the Raspberry Pi.
    The Pi posts one of these every 10-30 seconds.
    """
    __tablename__ = "sensor_readings"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key - links to User table (hardcoded to user_id=1 for now)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamp - when this reading was taken
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Battery charge level (0-100%)
    battery_level = Column(Integer, nullable=False)

    # Power source at the time of this reading
    power_source = Column(String, nullable=False)
    # Values: "grid" or "battery"

    # Electrical measurements from the Pi sensors
    voltage = Column(Float, nullable=True)
    # Measured in volts (e.g. 48.2V) - nullable in case Pi doesn't send it

    current = Column(Float, nullable=True)
    # Measured in amps (e.g. -2.5A)
    # Negative = discharging, Positive = charging
    # nullable in case Pi doesn't send it

    temperature = Column(Float, nullable=True)
    # Measured in Celsius - nullable in case Pi doesn't send it

    # Relationship back to User
    user = relationship("User", back_populates="sensor_readings")

    def __repr__(self):
        return f"<SensorReading(time={self.timestamp}, battery={self.battery_level}%, source={self.power_source})>"

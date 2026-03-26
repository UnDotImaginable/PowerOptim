"""
Pi routes - all communication between Raspberry Pi and backend lives here
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.sensor_reading import SensorReading
from schemas.sensor_reading import SensorReadingCreate
from utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/pi", tags=["Pi"])


@router.post("/readings")
async def receive_reading(payload: SensorReadingCreate, db: Session = Depends(get_db)):
    """
    Receives a sensor snapshot from the Raspberry Pi and saves it to the database.
    Pi should call this every 10-30 seconds.
    """
    logger.info(f"Received reading from Pi: battery={payload.battery_level}%, source={payload.power_source}")

    reading = SensorReading(
        user_id=1,  # Hardcoded until auth is built
        battery_level=payload.battery_level,
        power_source=payload.power_source,
        voltage=payload.voltage,
        current=payload.current,
        temperature=payload.temperature
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    logger.debug(f"Saved reading id={reading.id} at {reading.timestamp}")

    return {
        "success": True,
        "id": reading.id,
        "timestamp": reading.timestamp
    }
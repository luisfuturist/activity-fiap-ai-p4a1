import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# from sqlalchemy.orm import declarative_base
from db.database_session import get_db  # Import get_db function
from db.models import *
from db.database_session import Base

# # Base class for SQLAlchemy ORM
# Base = declarative_base()


# Database initialization
def init_db():
    with get_db() as db:
        Base.metadata.create_all(db.bind)


# Initial database population
def populate_db():
    with get_db() as db:
        try:
            # Initial data for PlantingArea
            areas = [
                PlantingArea(
                    area_name="Sector A",
                    size_hectares=10.5,
                    crop="Corn",
                    planting_date="2024-01-15",
                ),
                PlantingArea(
                    area_name="Sector B",
                    size_hectares=8.2,
                    crop="Soybean",
                    planting_date="2024-02-01",
                ),
            ]
            db.add_all(areas)

            harvests = [
                Harvest(
                    id_area=1,
                    planting_date="2024-07-15",
                    emergence_date="2024-03-10",
                    phenological_stage="R6",
                    yield_value=8500,
                ),
                Harvest(
                    id_area=2,
                    planting_date="2024-08-20",
                    emergence_date="2024-03-25",
                    phenological_stage="R6",
                    yield_value=9200,
                ),
            ]
            db.add_all(harvests)

            # Initial data for SensorType
            sensor_types = [
                SensorType(name="K", description="Sensor to measure Potassium level"),
                SensorType(name="P", description="Sensor to measure Phosphorus level"),
                SensorType(name="pH", description="Sensor to measure soil pH level"),
                SensorType(
                    name="Moisture", description="Sensor to measure soil moisture"
                ),
            ]
            db.add_all(sensor_types)

            # Initial data for Sensor
            sensors = [
                Sensor(id_type=1, id_area=1, sensor_name="Sensor K - Sector A"),
                Sensor(id_type=2, id_area=1, sensor_name="Sensor P - Sector A"),
                Sensor(id_type=3, id_area=1, sensor_name="Sensor pH - Sector A"),
                Sensor(id_type=4, id_area=1, sensor_name="Sensor Moisture - Sector A"),
                Sensor(id_type=1, id_area=2, sensor_name="Sensor K - Sector B"),
                Sensor(id_type=2, id_area=2, sensor_name="Sensor P - Sector B"),
                Sensor(id_type=3, id_area=2, sensor_name="Sensor pH - Sector B"),
                Sensor(id_type=4, id_area=2, sensor_name="Sensor Moisture - Sector B"),
            ]
            db.add_all(sensors)

            db.commit()
            print("Database populated successfully!")
        except Exception as e:
            db.rollback()
            print(f"Error populating the database: {e}")


if __name__ == "__main__":
    init_db()
    populate_db()

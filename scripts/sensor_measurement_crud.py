from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
from init_db import SensorMeasurement
from database_session import get_db
import datetime


class SensorMeasurementUpdate(TypedDict, total=False):
    id_sensor: int
    id_area: int
    id_harvest: int
    measurement: float
    datetime: datetime.datetime
    environmental_conditions: str


def create_sensor_measurement(
    id_sensor: int,
    id_area: int,
    id_harvest: int = None,
    measurement: float = None,
    datetime_str: str = None,
    environmental_conditions: str = None,
):
    """Creates a new SensorMeasurement entry."""
    with get_db() as db:
        try:
            measurement_datetime = (
                datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                if datetime_str
                else datetime.datetime.now()
            )

            new_measurement = SensorMeasurement(
                id_sensor=id_sensor,
                id_area=id_area,
                id_harvest=id_harvest,
                measurement=measurement,
                datetime=measurement_datetime,
                environmental_conditions=environmental_conditions,
            )
            db.add(new_measurement)
            db.commit()
            db.refresh(new_measurement)
            return new_measurement
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating SensorMeasurement: {e}")


def get_sensor_measurement(id_measurement: int):
    """Retrieves a SensorMeasurement entry by ID."""
    with get_db() as db:
        return db.query(SensorMeasurement).get(id_measurement)


def get_all_sensor_measurements():
    """Retrieves all SensorMeasurement entries."""
    with get_db() as db:
        return db.query(SensorMeasurement).all()


def get_sensor_measurements_by_sensor(id_sensor: int):
    """Retrieves all measurements for a specific sensor."""
    with get_db() as db:
        return (
            db.query(SensorMeasurement)
            .filter(SensorMeasurement.id_sensor == id_sensor)
            .all()
        )


def get_sensor_measurements_by_area(id_area: int):
    """Retrieves all measurements for a specific area."""
    with get_db() as db:
        return (
            db.query(SensorMeasurement)
            .filter(SensorMeasurement.id_area == id_area)
            .all()
        )


def update_sensor_measurement(id_measurement: int, updates: SensorMeasurementUpdate):
    """Updates a SensorMeasurement entry."""
    with get_db() as db:
        try:
            measurement = db.query(SensorMeasurement).get(id_measurement)
            if measurement:
                for key, value in updates.items():
                    setattr(measurement, key, value)
                db.commit()
                return measurement
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating SensorMeasurement: {e}")


def delete_sensor_measurement(id_measurement: int):
    """Deletes a SensorMeasurement entry."""
    with get_db() as db:
        try:
            measurement = db.query(SensorMeasurement).get(id_measurement)
            if measurement:
                db.delete(measurement)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting SensorMeasurement: {e}")


if __name__ == "__main__":
    # Test the functions
    new_measurement = create_sensor_measurement(
        id_sensor=1,
        id_area=1,
        measurement=10.5,
        datetime_str="2024-10-27 10:30:00",
        environmental_conditions="Sunny",
    )
    print(f"Created Sensor Measurement: {new_measurement}")

    retrieved_measurement = get_sensor_measurement(new_measurement.id_measurement)
    print(f"Retrieved Sensor Measurement: {retrieved_measurement}")

    all_measurements = get_all_sensor_measurements()
    print(f"All Sensor Measurements: {all_measurements}")

    measurements_sensor_1 = get_sensor_measurements_by_sensor(1)
    print(f"Measurements for Sensor 1: {measurements_sensor_1}")

    measurements_area_1 = get_sensor_measurements_by_area(1)
    print(f"Measurements for Area 1: {measurements_area_1}")

    updated_measurement = update_sensor_measurement(
        new_measurement.id_measurement, {"measurement": 11.0}
    )
    print(f"Updated Sensor Measurement: {updated_measurement}")

    # deleted = delete_sensor_measurement(new_measurement.id_measurement)
    # print(f"Deleted Sensor Measurement: {deleted}")

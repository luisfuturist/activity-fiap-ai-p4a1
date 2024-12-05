from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
from init_db import Sensor
from database_session import get_db


class SensorUpdate(TypedDict, total=False):
    id_type: int
    id_area: int
    sensor_name: str


def create_sensor(id_type: int, id_area: int, sensor_name: str):
    """Creates a new Sensor entry."""
    with get_db() as db:
        try:
            new_sensor = Sensor(
                id_type=id_type, id_area=id_area, sensor_name=sensor_name
            )
            db.add(new_sensor)
            db.commit()
            db.refresh(new_sensor)
            return new_sensor
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating Sensor: {e}")


def get_sensor(id_sensor: int):
    """Retrieves a Sensor entry by ID."""
    with get_db() as db:
        return db.query(Sensor).get(id_sensor)


def get_all_sensors():
    """Retrieves all Sensor entries."""
    with get_db() as db:
        return db.query(Sensor).all()


def get_sensors_by_area(id_area: int):
    """Retrieves all sensors for a specific area."""
    with get_db() as db:
        return db.query(Sensor).filter(Sensor.id_area == id_area).all()


def get_sensors_by_type(id_type: int):
    """Retrieves all sensors of a specific type."""
    with get_db() as db:
        return db.query(Sensor).filter(Sensor.id_type == id_type).all()


def update_sensor(id_sensor: int, updates: SensorUpdate):
    """Updates a Sensor entry."""
    with get_db() as db:
        try:
            sensor = db.query(Sensor).get(id_sensor)
            if sensor:
                for key, value in updates.items():
                    setattr(sensor, key, value)
                db.commit()
                return sensor
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating Sensor: {e}")


def delete_sensor(id_sensor: int):
    """Deletes a Sensor entry."""
    with get_db() as db:
        try:
            sensor = db.query(Sensor).get(id_sensor)
            if sensor:
                db.delete(sensor)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting Sensor: {e}")


if __name__ == "__main__":
    # Test the functions
    new_sensor = create_sensor(id_type=1, id_area=1, sensor_name="Sensor K - Test")
    print(f"Created Sensor: {new_sensor}")

    retrieved_sensor = get_sensor(new_sensor.id_sensor)
    print(f"Retrieved Sensor: {retrieved_sensor}")

    all_sensors = get_all_sensors()
    print(f"All Sensors: {all_sensors}")

    sensors_area_1 = get_sensors_by_area(1)
    print(f"Sensors in Area 1: {sensors_area_1}")

    sensors_type_1 = get_sensors_by_type(1)
    print(f"Sensors of Type 1: {sensors_type_1}")

    updated_sensor = update_sensor(
        new_sensor.id_sensor, {"sensor_name": "Updated Sensor Name"}
    )
    print(f"Updated Sensor: {updated_sensor}")

    # deleted = delete_sensor(new_sensor.id_sensor)
    # print(f"Deleted Sensor: {deleted}")

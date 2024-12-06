from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
from db.models import SensorType
from db.database_session import get_db


class SensorTypeUpdate(TypedDict, total=False):
    name: str
    description: str


def create_sensor_type(name: str, description: str = None):
    """Creates a new SensorType entry."""
    with get_db() as db:
        try:
            new_sensor_type = SensorType(name=name, description=description)
            db.add(new_sensor_type)
            db.commit()
            db.refresh(new_sensor_type)
            return new_sensor_type
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating SensorType: {e}")


def get_sensor_type(id_type: int):
    """Retrieves a SensorType entry by ID."""
    with get_db() as db:
        return db.query(SensorType).get(id_type)


def get_all_sensor_types():
    """Retrieves all SensorType entries."""
    with get_db() as db:
        return db.query(SensorType).all()


def get_sensor_type_by_name(name: str):
    """Retrieves a SensorType entry by name."""
    with get_db() as db:
        return db.query(SensorType).filter(SensorType.name == name).first()


def update_sensor_type(id_type: int, updates: SensorTypeUpdate):
    """Updates a SensorType entry."""
    with get_db() as db:
        try:
            sensor_type = db.query(SensorType).get(id_type)
            if sensor_type:
                for key, value in updates.items():
                    setattr(sensor_type, key, value)
                db.commit()
                return sensor_type
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating SensorType: {e}")


def delete_sensor_type(id_type: int):
    """Deletes a SensorType entry."""
    with get_db() as db:
        try:
            sensor_type = db.query(SensorType).get(id_type)
            if sensor_type:
                db.delete(sensor_type)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting SensorType: {e}")


if __name__ == "__main__":
    # Test the functions
    new_sensor_type = create_sensor_type("Temperature", "Measures soil temperature")
    print(f"Created Sensor Type: {new_sensor_type}")

    retrieved_sensor_type = get_sensor_type(new_sensor_type.id_type)
    print(f"Retrieved Sensor Type: {retrieved_sensor_type}")

    all_sensor_types = get_all_sensor_types()
    print(f"All Sensor Types: {all_sensor_types}")

    sensor_type_by_name = get_sensor_type_by_name("Temperature")
    print(f"Sensor Type by name: {sensor_type_by_name}")

    updated_sensor_type = update_sensor_type(
        new_sensor_type.id_type, {"description": "Measures soil temperature in Celsius"}
    )
    print(f"Updated Sensor Type: {updated_sensor_type}")

    # deleted = delete_sensor_type(new_sensor_type.id_type)
    # print(f"Deleted Sensor Type: {deleted}")

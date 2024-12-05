from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
from .init_db import PlantingArea
from .database_session import get_db
import datetime


class PlantingAreaUpdate(TypedDict, total=False):  # total=False allows partial updates
    area_name: str
    size_hectares: float
    crop: str
    planting_date: datetime.date


def create_planting_area(
    area_name: str, size_hectares: float, crop: str, planting_date: str
):
    """Creates a new PlantingArea entry."""
    with get_db() as db:
        try:
            new_area = PlantingArea(
                area_name=area_name,
                size_hectares=size_hectares,
                crop=crop,
                planting_date=datetime.datetime.strptime(
                    planting_date, "%Y-%m-%d"
                ).date(),
            )
            db.add(new_area)
            db.commit()
            db.refresh(new_area)
            return new_area
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating PlantingArea: {e}")


def get_planting_area(id_area: int):
    """Retrieves a PlantingArea entry by ID."""
    with get_db() as db:
        return db.query(PlantingArea).get(id_area)


def get_all_planting_areas():
    """Retrieves all PlantingArea entries."""
    with get_db() as db:
        return db.query(PlantingArea).all()


def update_planting_area(id_area: int, updates: PlantingAreaUpdate):
    """Updates a PlantingArea entry."""
    with get_db() as db:
        try:
            area = db.query(PlantingArea).get(id_area)
            if area:
                update_data = updates.model_dump(
                    exclude_unset=True
                )  # Only update set fields
                for key, value in update_data.items():
                    setattr(area, key, value)
                db.commit()
                return area
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating PlantingArea: {e}")


def delete_planting_area(id_area: int):
    """Deletes a PlantingArea entry."""
    with get_db() as db:
        try:
            area = db.query(PlantingArea).get(id_area)
            if area:
                db.delete(area)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting PlantingArea: {e}")


if __name__ == "__main__":
    # Test the functions
    new_area = create_planting_area("Area B", 12.0, "Wheat", "2024-04-10")
    print(f"Created Planting Area: {new_area}")

    retrieved_area = get_planting_area(new_area.id_area)
    print(f"Retrieved Planting Area: {retrieved_area}")

    all_areas = get_all_planting_areas()
    print(f"All Planting Areas: {all_areas}")

    updated_area = update_planting_area(new_area.id_area, {"crop": "Barley"})
    print(f"Updated Planting Area: {updated_area}")

    deleted = delete_planting_area(new_area.id_area)
    print(f"Deleted Planting Area: {deleted}")

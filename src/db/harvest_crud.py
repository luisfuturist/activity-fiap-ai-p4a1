from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
import datetime
from db.models import Harvest
from db.database_session import get_db


class HarvestUpdate(TypedDict, total=False):
    planting_date: datetime.date
    harvest_date: datetime.date
    emergence_date: datetime.date
    phenological_stage: str
    yield_value: float


def create_harvest(
    id_area: int,
    planting_date: str,
    harvest_date: str = None,
    emergence_date: str = None,
    phenological_stage: str = None,
    yield_value: float = None,
):
    """Creates a new Harvest entry."""
    with get_db() as db:
        try:
            new_harvest = Harvest(
                id_area=id_area,
                planting_date=datetime.datetime.strptime(
                    planting_date, "%Y-%m-%d"
                ).date(),
                harvest_date=(
                    datetime.datetime.strptime(harvest_date, "%Y-%m-%d").date()
                    if harvest_date
                    else None
                ),
                emergence_date=(
                    datetime.datetime.strptime(emergence_date, "%Y-%m-%d").date()
                    if emergence_date
                    else None
                ),
                phenological_stage=phenological_stage,
                yield_value=yield_value,
            )
            db.add(new_harvest)
            db.commit()
            db.refresh(new_harvest)
            return new_harvest
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating Harvest: {e}")


def get_harvest(id_harvest: int):
    """Retrieves a Harvest entry by ID."""
    with get_db() as db:
        return db.query(Harvest).get(id_harvest)


def get_all_harvests():
    """Retrieves all Harvest entries."""
    with get_db() as db:
        return db.query(Harvest).all()


def get_harvests_by_area(id_area: int):
    """Retrieves all Harvest entries for a specific area."""
    with get_db() as db:
        return db.query(Harvest).filter(Harvest.id_area == id_area).all()


def update_harvest(id_harvest: int, updates: HarvestUpdate):
    """Updates a Harvest entry."""
    with get_db() as db:
        try:
            harvest = db.query(Harvest).get(id_harvest)
            if harvest:
                for key, value in updates.items():
                    setattr(harvest, key, value)
                db.commit()
                return harvest
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating Harvest: {e}")


def delete_harvest(id_harvest: int):
    """Deletes a Harvest entry."""
    with get_db() as db:
        try:
            harvest = db.query(Harvest).get(id_harvest)
            if harvest:
                db.delete(harvest)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting Harvest: {e}")


if __name__ == "__main__":
    # Test the functions
    new_harvest = create_harvest(
        id_area=1,
        planting_date="2024-03-15",
        harvest_date="2024-07-15",
        yield_value=8500,
    )
    print(f"Created Harvest: {new_harvest}")

    retrieved_harvest = get_harvest(new_harvest.id_harvest)
    print(f"Retrieved Harvest: {retrieved_harvest}")

    all_harvests = get_all_harvests()
    print(f"All Harvests: {all_harvests}")

    harvests_area_1 = get_harvests_by_area(1)
    print(f"Harvests in Area 1: {harvests_area_1}")

    updated_harvest = update_harvest(new_harvest.id_harvest, {"yield_value": 8700})
    print(f"Updated Harvest: {updated_harvest}")

    # deleted = delete_harvest(new_harvest.id_harvest)
    # print(f"Deleted Harvest: {deleted}")

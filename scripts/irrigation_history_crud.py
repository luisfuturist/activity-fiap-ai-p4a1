from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
from init_db import IrrigationHistory
from database_session import get_db
import datetime


class IrrigationHistoryUpdate(TypedDict, total=False):
    id_area: int
    id_recommendation: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    water_volume: float


def create_irrigation_history(
    id_area: int,
    id_recommendation: int,
    start_time: str,
    end_time: str,
    water_volume: float,
):
    """Creates a new IrrigationHistory entry."""
    with get_db() as db:
        try:
            start_time_obj = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time_obj = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

            new_history = IrrigationHistory(
                id_area=id_area,
                id_recommendation=id_recommendation,
                start_time=start_time_obj,
                end_time=end_time_obj,
                water_volume=water_volume,
            )
            db.add(new_history)
            db.commit()
            db.refresh(new_history)
            return new_history
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating IrrigationHistory: {e}")


def get_irrigation_history(id_irrigation: int):
    """Retrieves a IrrigationHistory entry by ID."""
    with get_db() as db:
        return db.query(IrrigationHistory).get(id_irrigation)


def get_all_irrigation_histories():
    """Retrieves all IrrigationHistory entries."""
    with get_db() as db:
        return db.query(IrrigationHistory).all()


def get_history_by_area(id_area: int):
    """Retrieves irrigation history for a specific area."""
    with get_db() as db:
        return (
            db.query(IrrigationHistory)
            .filter(IrrigationHistory.id_area == id_area)
            .all()
        )


def get_history_by_recommendation(id_recommendation: int):
    """Retrieves irrigation history for a specific recommendation."""
    with get_db() as db:
        return (
            db.query(IrrigationHistory)
            .filter(IrrigationHistory.id_recommendation == id_recommendation)
            .all()
        )


def update_irrigation_history(id_irrigation: int, updates: IrrigationHistoryUpdate):
    """Updates a IrrigationHistory entry."""
    with get_db() as db:
        try:
            history = db.query(IrrigationHistory).get(id_irrigation)
            if history:
                for key, value in updates.items():
                    setattr(history, key, value)
                db.commit()
                return history
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating IrrigationHistory: {e}")


def delete_irrigation_history(id_irrigation: int):
    """Deletes a IrrigationHistory entry."""
    with get_db() as db:
        try:
            history = db.query(IrrigationHistory).get(id_irrigation)
            if history:
                db.delete(history)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting IrrigationHistory: {e}")


if __name__ == "__main__":
    # Test the functions
    new_history = create_irrigation_history(
        id_area=1,
        id_recommendation=1,
        start_time="2024-10-27 17:00:00",
        end_time="2024-10-27 18:00:00",
        water_volume=5000,
    )
    print(f"Created Irrigation History: {new_history}")

    retrieved_history = get_irrigation_history(new_history.id_irrigation)
    print(f"Retrieved Irrigation History: {retrieved_history}")

    all_histories = get_all_irrigation_histories()
    print(f"All Irrigation Histories: {all_histories}")

    history_area_1 = get_history_by_area(1)
    print(f"Irrigation History for Area 1: {history_area_1}")

    history_recommendation_1 = get_history_by_recommendation(1)
    print(f"Irrigation History for Recommendation 1: {history_recommendation_1}")

    updated_history = update_irrigation_history(
        new_history.id_irrigation, {"water_volume": 5500}
    )
    print(f"Updated Irrigation History: {updated_history}")

    # deleted = delete_irrigation_history(new_history.id_irrigation)
    # print(f"Deleted Irrigation History: {deleted}")

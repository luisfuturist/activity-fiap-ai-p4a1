from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
from init_db import IrrigationRecommendation
from database_session import get_db
import datetime


class IrrigationRecommendationUpdate(TypedDict, total=False):
    id_model: int
    id_area: int
    recommendation_date: datetime.datetime
    irrigation_needed: bool


def create_irrigation_recommendation(
    id_model: int,
    id_area: int,
    irrigation_needed: bool,
    recommendation_date: str = None,
):
    """Creates a new IrrigationRecommendation entry."""
    with get_db() as db:
        try:
            recommendation_date_obj = (
                datetime.datetime.strptime(recommendation_date, "%Y-%m-%d %H:%M:%S")
                if recommendation_date
                else datetime.datetime.now()
            )

            new_recommendation = IrrigationRecommendation(
                id_model=id_model,
                id_area=id_area,
                recommendation_date=recommendation_date_obj,
                irrigation_needed=irrigation_needed,
            )
            db.add(new_recommendation)
            db.commit()
            db.refresh(new_recommendation)
            return new_recommendation
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating IrrigationRecommendation: {e}")


def get_irrigation_recommendation(id_recommendation: int):
    """Retrieves a IrrigationRecommendation entry by ID."""
    with get_db() as db:
        return db.query(IrrigationRecommendation).get(id_recommendation)


def get_all_irrigation_recommendations():
    """Retrieves all IrrigationRecommendation entries."""
    with get_db() as db:
        return db.query(IrrigationRecommendation).all()


def get_recommendations_by_area(id_area: int):
    """Retrieves all recommendations for a specific area."""
    with get_db() as db:
        return (
            db.query(IrrigationRecommendation)
            .filter(IrrigationRecommendation.id_area == id_area)
            .all()
        )


def get_recommendations_by_model(id_model: int):
    """Retrieves all recommendations made by a specific model."""
    with get_db() as db:
        return (
            db.query(IrrigationRecommendation)
            .filter(IrrigationRecommendation.id_model == id_model)
            .all()
        )


def update_irrigation_recommendation(
    id_recommendation: int, updates: IrrigationRecommendationUpdate
):
    """Updates a IrrigationRecommendation entry."""
    with get_db() as db:
        try:
            recommendation = db.query(IrrigationRecommendation).get(id_recommendation)
            if recommendation:
                for key, value in updates.items():
                    setattr(recommendation, key, value)
                db.commit()
                return recommendation
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating IrrigationRecommendation: {e}")


def delete_irrigation_recommendation(id_recommendation: int):
    """Deletes a IrrigationRecommendation entry."""
    with get_db() as db:
        try:
            recommendation = db.query(IrrigationRecommendation).get(id_recommendation)
            if recommendation:
                db.delete(recommendation)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting IrrigationRecommendation: {e}")


if __name__ == "__main__":
    # Test the functions
    new_recommendation = create_irrigation_recommendation(
        id_model=1,
        id_area=1,
        irrigation_needed=True,
        recommendation_date="2024-10-27 16:00:00",
    )
    print(f"Created Irrigation Recommendation: {new_recommendation}")

    retrieved_recommendation = get_irrigation_recommendation(
        new_recommendation.id_recommendation
    )
    print(f"Retrieved Irrigation Recommendation: {retrieved_recommendation}")

    all_recommendations = get_all_irrigation_recommendations()
    print(f"All Irrigation Recommendations: {all_recommendations}")

    recommendations_area_1 = get_recommendations_by_area(1)
    print(f"Recommendations for Area 1: {recommendations_area_1}")

    recommendations_model_1 = get_recommendations_by_model(1)
    print(f"Recommendations for Model 1: {recommendations_model_1}")

    updated_recommendation = update_irrigation_recommendation(
        new_recommendation.id_recommendation, {"irrigation_needed": False}
    )
    print(f"Updated Irrigation Recommendation: {updated_recommendation}")

    # deleted = delete_irrigation_recommendation(new_recommendation.id_recommendation)
    # print(f"Deleted Irrigation Recommendation: {deleted}")

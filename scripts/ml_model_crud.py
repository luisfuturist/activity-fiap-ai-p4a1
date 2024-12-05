from typing import TypedDict
from sqlalchemy.exc import SQLAlchemyError
from init_db import MLModel
from database_session import get_db
import datetime


class MLModelUpdate(TypedDict, total=False):
    model_name: str
    model_type: str
    training_date: datetime.datetime
    model_parameters: str
    ml_library: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float


def create_ml_model(
    model_name: str,
    model_type: str,
    model_parameters: str,
    ml_library: str,
    accuracy: float,
    precision: float,
    recall: float,
    f1_score: float,
    training_date: str = None,
):
    """Creates a new MLModel entry."""
    with get_db() as db:
        try:
            training_date_obj = (
                datetime.datetime.strptime(training_date, "%Y-%m-%d %H:%M:%S")
                if training_date
                else datetime.datetime.now()
            )

            new_model = MLModel(
                model_name=model_name,
                model_type=model_type,
                training_date=training_date_obj,
                model_parameters=model_parameters,
                ml_library=ml_library,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=f1_score,
            )
            db.add(new_model)
            db.commit()
            db.refresh(new_model)
            return new_model
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error creating MLModel: {e}")


def get_ml_model(id_model: int):
    """Retrieves a MLModel entry by ID."""
    with get_db() as db:
        return db.query(MLModel).get(id_model)


def get_all_ml_models():
    """Retrieves all MLModel entries."""
    with get_db() as db:
        return db.query(MLModel).all()


def update_ml_model(id_model: int, updates: MLModelUpdate):
    """Updates a MLModel entry."""
    with get_db() as db:
        try:
            model = db.query(MLModel).get(id_model)
            if model:
                for key, value in updates.items():
                    setattr(model, key, value)
                db.commit()
                return model
            else:
                return None
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error updating MLModel: {e}")


def delete_ml_model(id_model: int):
    """Deletes a MLModel entry."""
    with get_db() as db:
        try:
            model = db.query(MLModel).get(id_model)
            if model:
                db.delete(model)
                db.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error deleting MLModel: {e}")


if __name__ == "__main__":
    # Test the functions
    new_model = create_ml_model(
        model_name="Model A",
        model_type="Regression",
        model_parameters="{'param1': 1, 'param2': 2}",
        ml_library="scikit-learn",
        accuracy=0.95,
        precision=0.92,
        recall=0.90,
        f1_score=0.91,
        training_date="2024-10-26 15:00:00",
    )
    print(f"Created ML Model: {new_model}")

    retrieved_model = get_ml_model(new_model.id_model)
    print(f"Retrieved ML Model: {retrieved_model}")

    all_models = get_all_ml_models()
    print(f"All ML Models: {all_models}")

    updated_model = update_ml_model(new_model.id_model, {"accuracy": 0.96})
    print(f"Updated ML Model: {updated_model}")

    # deleted = delete_ml_model(new_model.id_model)
    # print(f"Deleted ML Model: {deleted}")

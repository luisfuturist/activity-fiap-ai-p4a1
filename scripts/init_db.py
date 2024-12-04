from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    Text,
    ForeignKey,
    TIMESTAMP,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Database connection details
DATABASE_URL = "postgresql://fiap_p4a1:fiap_p4a1@localhost:5433/fiap_p4a1"

# Base class for SQLAlchemy ORM
Base = declarative_base()

# Setup the database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Table definitions as SQLAlchemy classes


class PlantingArea(Base):
    __tablename__ = "Planting_Area"
    id_area = Column(Integer, primary_key=True, autoincrement=True)
    area_name = Column(String, nullable=False)
    size_hectares = Column(Float)
    crop = Column(String)
    planting_date = Column(Date)


class Harvest(Base):
    __tablename__ = "Harvest"
    id_harvest = Column(Integer, primary_key=True, autoincrement=True)
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"), nullable=False)
    planting_date = Column(Date, nullable=False)
    harvest_date = Column(Date)
    emergence_date = Column(Date)
    phenological_stage = Column(String)  # e.g., 'V6', 'R1', 'R6'
    yield_value = Column(Float)  # e.g., kg/ha or tons/ha
    area = relationship("PlantingArea")


class SensorType(Base):
    __tablename__ = "Sensor_Type"
    id_type = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)


class Sensor(Base):
    __tablename__ = "Sensor"
    id_sensor = Column(Integer, primary_key=True, autoincrement=True)
    id_type = Column(Integer, ForeignKey("Sensor_Type.id_type"), nullable=False)
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"), nullable=False)
    sensor_name = Column(String, nullable=False)
    sensor_type = relationship("SensorType")
    planting_area = relationship("PlantingArea")


class SensorMeasurement(Base):
    __tablename__ = "Sensor_Measurement"
    id_measurement = Column(Integer, primary_key=True, autoincrement=True)
    id_sensor = Column(Integer, ForeignKey("Sensor.id_sensor"), nullable=False)
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"), nullable=False)
    id_harvest = Column(Integer, ForeignKey("Harvest.id_harvest"), nullable=True)
    measurement = Column(Float)
    datetime = Column(TIMESTAMP, default=func.current_timestamp())
    environmental_conditions = Column(String)
    sensor = relationship("Sensor")
    area = relationship("PlantingArea")
    harvest = relationship("Harvest")


class MLModel(Base):
    __tablename__ = "ML_Model"
    id_model = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String, nullable=False)
    model_type = Column(String, nullable=False)
    training_date = Column(TIMESTAMP, default=func.current_timestamp())
    model_parameters = Column(Text)
    ml_library = Column(String, nullable=False)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)


class IrrigationRecommendation(Base):
    __tablename__ = "Irrigation_Recommendation"
    id_recommendation = Column(Integer, primary_key=True, autoincrement=True)
    id_model = Column(Integer, ForeignKey("ML_Model.id_model"))
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"))
    recommendation_date = Column(TIMESTAMP, default=func.current_timestamp())
    irrigation_needed = Column(Boolean)
    model_ml = relationship("MLModel")
    area = relationship("PlantingArea")


class IrrigationHistory(Base):
    __tablename__ = "Irrigation_History"
    id_irrigation = Column(Integer, primary_key=True, autoincrement=True)
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"))
    id_recommendation = Column(
        Integer, ForeignKey("Irrigation_Recommendation.id_recommendation")
    )
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    water_volume = Column(Float)
    area = relationship("PlantingArea")
    recommendation = relationship("IrrigationRecommendation")


# Database initialization
def init_db():
    Base.metadata.create_all(engine)


# Initial database population
def populate_db():
    session = Session()
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
        session.add_all(areas)

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
        session.add_all(harvests)

        # Initial data for SensorType
        sensor_types = [
            SensorType(name="K", description="Sensor to measure Potassium level"),
            SensorType(name="P", description="Sensor to measure Phosphorus level"),
            SensorType(name="pH", description="Sensor to measure soil pH level"),
            SensorType(name="Moisture", description="Sensor to measure soil moisture"),
        ]
        session.add_all(sensor_types)

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
        session.add_all(sensors)

        session.commit()
        print("Database populated successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error populating the database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    populate_db()

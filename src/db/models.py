from sqlalchemy import (
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
from sqlalchemy.orm import relationship, declarative_base
from db.database_session import Base

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
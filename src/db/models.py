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
from sqlalchemy.orm import relationship
from db.database_session import Base


class PlantingArea(Base):
    __tablename__ = "Planting_Area"
    id_area = Column(Integer, primary_key=True, autoincrement=True)
    area_name = Column(String, nullable=False)
    size_hectares = Column(Float)
    planting_date = Column(Date)

    def __repr__(self):
        return f"<PlantingArea(id_area={self.id_area}, area_name={self.area_name}, size_hectares={self.size_hectares}, planting_date={self.planting_date})>"


class Harvest(Base):
    __tablename__ = "Harvest"
    id_harvest = Column(Integer, primary_key=True, autoincrement=True)
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"), nullable=False)
    crop = Column(String)
    planting_date = Column(Date, nullable=False)
    harvest_date = Column(Date)
    emergence_date = Column(Date)
    phenological_stage = Column(String)  # e.g., 'V6', 'R1', 'R6'
    yield_value = Column(Float)  # e.g., kg/ha or tons/ha
    area = relationship("PlantingArea")

    def __repr__(self):
        return f"<Harvest(id_harvest={self.id_harvest}, id_area={self.id_area}, crop={self.crop}, planting_date={self.planting_date}, harvest_date={self.harvest_date}, emergence_date={self.emergence_date}, phenological_stage={self.phenological_stage}, yield_value={self.yield_value})>"


class SensorType(Base):
    __tablename__ = "Sensor_Type"
    id_type = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    def __repr__(self):
        return f"<SensorType(id_type={self.id_type}, name={self.name}, description={self.description})>"


class Sensor(Base):
    __tablename__ = "Sensor"
    id_sensor = Column(Integer, primary_key=True, autoincrement=True)
    id_type = Column(Integer, ForeignKey("Sensor_Type.id_type"), nullable=False)
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"), nullable=False)
    sensor_name = Column(String, nullable=False)
    sensor_type = relationship("SensorType")
    planting_area = relationship("PlantingArea")

    def __repr__(self):
        return f"<Sensor(id_sensor={self.id_sensor}, id_type={self.id_type}, id_area={self.id_area}, sensor_name={self.sensor_name})>"


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

    def __repr__(self):
        return f"<SensorMeasurement(id_measurement={self.id_measurement}, id_sensor={self.id_sensor}, id_area={self.id_area}, id_harvest={self.id_harvest}, measurement={self.measurement}, datetime={self.datetime}, environmental_conditions={self.environmental_conditions})>"


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

    def __repr__(self):
        return f"<MLModel(id_model={self.id_model}, model_name={self.model_name}, model_type={self.model_type}, training_date={self.training_date}, model_parameters={self.model_parameters}, ml_library={self.ml_library}, accuracy={self.accuracy}, precision={self.precision}, recall={self.recall}, f1_score={self.f1_score})>"


class IrrigationRecommendation(Base):
    __tablename__ = "Irrigation_Recommendation"
    id_recommendation = Column(Integer, primary_key=True, autoincrement=True)
    id_model = Column(Integer, ForeignKey("ML_Model.id_model"))
    id_area = Column(Integer, ForeignKey("Planting_Area.id_area"))
    recommendation_date = Column(TIMESTAMP, default=func.current_timestamp())
    irrigation_needed = Column(Boolean)
    model_ml = relationship("MLModel")
    area = relationship("PlantingArea")

    def __repr__(self):
        return f"<IrrigationRecommendation(id_recommendation={self.id_recommendation}, id_model={self.id_model}, id_area={self.id_area}, recommendation_date={self.recommendation_date}, irrigation_needed={self.irrigation_needed})>"


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

    def __repr__(self):
        return f"<IrrigationHistory(id_irrigation={self.id_irrigation}, id_area={self.id_area}, id_recommendation={self.id_recommendation}, start_time={self.start_time}, end_time={self.end_time}, water_volume={self.water_volume})>"

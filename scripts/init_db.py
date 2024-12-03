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
DATABASE_URL = "postgresql://fiap_p4a1:fiap_p4a1@localhost:5432/fiap_p4a1"

# Base class for SQLAlchemy ORM
Base = declarative_base()

# Setup the database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Definição das tabelas como classes do SQLAlchemy


class AreaPlantio(Base):
    __tablename__ = "Area_Plantio"
    id_area = Column(Integer, primary_key=True, autoincrement=True)
    nome_area = Column(String, nullable=False)
    tamanho_hectares = Column(Float)
    cultura = Column(String)
    data_plantio = Column(Date)


class Colheita(Base):
    __tablename__ = "Colheita"
    id_colheita = Column(Integer, primary_key=True, autoincrement=True)
    id_area = Column(Integer, ForeignKey("Area_Plantio.id_area"), nullable=False)
    data_colheita = Column(Date, nullable=False)
    data_emergencia = Column(Date)
    estadio_fenologico = Column(String)  # e.g., 'V6', 'R1', 'R6'
    produtividade = Column(Float)  # e.g., kg/ha or tons/ha
    area = relationship("AreaPlantio")
    # Add other relevant fields as needed (e.g., yield, quality metrics, etc.)


class TipoSensor(Base):
    __tablename__ = "Tipo_Sensor"
    id_tipo = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)


class Sensor(Base):
    __tablename__ = "Sensor"
    id_sensor = Column(Integer, primary_key=True, autoincrement=True)
    id_tipo = Column(Integer, ForeignKey("Tipo_Sensor.id_tipo"), nullable=False)
    id_area_atual = Column(Integer, ForeignKey("Area_Plantio.id_area"), nullable=False)
    nome_sensor = Column(String, nullable=False)
    tipo_sensor = relationship("TipoSensor")
    area_plantio = relationship("AreaPlantio")


class MedicaoSensor(Base):
    __tablename__ = "Medicao_Sensor"
    id_medicao = Column(Integer, primary_key=True, autoincrement=True)
    id_sensor = Column(Integer, ForeignKey("Sensor.id_sensor"), nullable=False)
    id_area = Column(Integer, ForeignKey("Area_Plantio.id_area"), nullable=False)
    id_colheita = Column(Integer, ForeignKey("Colheita.id_colheita"), nullable=True)
    valor = Column(Float)
    data_hora = Column(TIMESTAMP, default=func.current_timestamp())
    condicoes_ambiente = Column(String)
    sensor = relationship("Sensor")
    area = relationship("AreaPlantio")
    colheita = relationship("Colheita")


class ModeloML(Base):
    __tablename__ = "Modelo_ML"
    id_modelo = Column(Integer, primary_key=True, autoincrement=True)
    nome_modelo = Column(String, nullable=False)
    tipo_modelo = Column(String, nullable=False)
    data_treinamento = Column(TIMESTAMP, default=func.current_timestamp())
    parametros_modelo = Column(Text)
    biblioteca_ml = Column(String, nullable=False)


class MetricasModelo(Base):
    __tablename__ = "Metricas_Modelo"
    id_metrica = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo = Column(Integer, ForeignKey("Modelo_ML.id_modelo"))
    metrica = Column(String, nullable=False)
    valor_metrica = Column(Float)
    modelo_ml = relationship("ModeloML")


class RecomendacaoIrrigacao(Base):
    __tablename__ = "Recomendacao_Irrigacao"
    id_recomendacao = Column(Integer, primary_key=True, autoincrement=True)
    id_modelo = Column(Integer, ForeignKey("Modelo_ML.id_modelo"))
    id_area = Column(Integer, ForeignKey("Area_Plantio.id_area"))
    data_recomendacao = Column(TIMESTAMP, default=func.current_timestamp())
    necessidade_irrigacao = Column(Boolean)
    modelo_ml = relationship("ModeloML")
    area = relationship("AreaPlantio")


class HistoricoIrrigacao(Base):
    __tablename__ = "Historico_Irrigacao"
    id_irrigacao = Column(Integer, primary_key=True, autoincrement=True)
    id_area = Column(Integer, ForeignKey("Area_Plantio.id_area"))
    id_recomendacao = Column(
        Integer, ForeignKey("Recomendacao_Irrigacao.id_recomendacao")
    )
    hora_inicio = Column(TIMESTAMP)
    hora_fim = Column(TIMESTAMP)
    volume_agua = Column(Float)
    area = relationship("AreaPlantio")
    recomendacao = relationship("RecomendacaoIrrigacao")


# Inicialização do banco de dados
def init_db():
    Base.metadata.create_all(engine)


# População inicial do banco de dados
def populate_db():
    session = Session()
    try:
        # Dados iniciais para AreaPlantio
        areas = [
            AreaPlantio(
                nome_area="Setor A",
                tamanho_hectares=10.5,
                cultura="Milho",
                data_plantio="2024-01-15",
            ),
            AreaPlantio(
                nome_area="Setor B",
                tamanho_hectares=8.2,
                cultura="Soja",
                data_plantio="2024-02-01",
            ),
        ]
        session.add_all(areas)

        colheitas = [
            Colheita(
                id_area=1,
                data_colheita="2024-07-15",
                data_emergencia="2024-03-10",
                estadio_fenologico="R6",
                produtividade=8500,
            ),
            Colheita(
                id_area=2,
                data_colheita="2024-08-20",
                data_emergencia="2024-03-25",
                estadio_fenologico="R6",
                produtividade=9200,
            ),
        ]
        session.add_all(colheitas)

        # Dados iniciais para TipoSensor
        tipos_sensores = [
            TipoSensor(nome="K", descricao="Sensor para medir o nível de Potássio"),
            TipoSensor(nome="P", descricao="Sensor para medir o nível de Fósforo"),
            TipoSensor(nome="pH", descricao="Sensor para medir o nível de pH do solo"),
            TipoSensor(nome="Umidade", descricao="Sensor para medir a umidade do solo"),
        ]
        session.add_all(tipos_sensores)

        # Dados iniciais para Sensor
        sensores = [
            Sensor(id_tipo=1, id_area_atual=1, nome_sensor="Sensor K - Setor A"),
            Sensor(id_tipo=2, id_area_atual=1, nome_sensor="Sensor P - Setor A"),
            Sensor(id_tipo=3, id_area_atual=1, nome_sensor="Sensor pH - Setor A"),
            Sensor(id_tipo=4, id_area_atual=1, nome_sensor="Sensor Umidade - Setor A"),
            Sensor(id_tipo=1, id_area_atual=2, nome_sensor="Sensor K - Setor B"),
            Sensor(id_tipo=2, id_area_atual=2, nome_sensor="Sensor P - Setor B"),
            Sensor(id_tipo=3, id_area_atual=2, nome_sensor="Sensor pH - Setor B"),
            Sensor(id_tipo=4, id_area_atual=2, nome_sensor="Sensor Umidade - Setor B"),
        ]
        session.add_all(sensores)

        session.commit()
        print("Banco de dados populado com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao popular o banco de dados: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    populate_db()

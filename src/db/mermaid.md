# Diagrama ER com Mermaid

Este documento contém um diagrama de entidade-relacionamento (ER) gerado usando a sintaxe do Mermaid.

O Mermaid é uma ferramenta que permite criar diagramas e gráficos de forma simples e rápida, utilizando uma linguagem de marcação semelhante ao Markdown. 

O Mermaid é suportado em várias plataformas, incluindo GitHub, GitLab, Bitbucket e Markdown Preview Enhanced. Portanto, o diagrama a seguir aparecerá corretamente quando visualizado em um desses ambientes.

Abaixo segue o diagrama ER gerado para o projeto Planting Area:



```mermaid
erDiagram
    Planting_Area ||--o{ Harvest : "has"
    Planting_Area ||--o{ Sensor : "has"
    Planting_Area ||--o{ Sensor_Measurement : "has"
    Planting_Area ||--o{ Irrigation_Recommendation : "has"
    Planting_Area ||--o{ Irrigation_History : "has"

    Harvest ||--o{ Sensor_Measurement : "has measurements"

    Sensor_Type ||--o{ Sensor : "defines"

    Sensor ||--o{ Sensor_Measurement : "records"
    Sensor }o--|| Planting_Area : "installed in"
    Sensor }o--|| Sensor_Type : "is of type"

    ML_Model ||--o{ Irrigation_Recommendation : "generates"

    Irrigation_Recommendation ||--o{ Irrigation_History : "logs"
    Irrigation_Recommendation }o--|| Planting_Area : "for"
    Irrigation_Recommendation }o--|| ML_Model : "by"

    Planting_Area {
        int id_area PK
        string area_name
        float size_hectares
        date planting_date
    }

    Harvest {
        int id_harvest PK
        int id_area FK
        string crop
        date planting_date
        date harvest_date
        date emergence_date
        string phenological_stage
        float yield_value
    }

    Sensor_Type {
        int id_type PK
        string name
        string description
    }

    Sensor {
        int id_sensor PK
        int id_type FK
        int id_area FK
        string sensor_name
    }

    Sensor_Measurement {
        int id_measurement PK
        int id_sensor FK
        int id_area FK
        int id_harvest FK
        float measurement
        timestamp datetime
        string environmental_conditions
    }

    ML_Model {
        int id_model PK
        string model_name
        string model_type
        timestamp training_date
        text model_parameters
        string ml_library
        float accuracy
        float precision
        float recall
        float f1_score
    }

    Irrigation_Recommendation {
        int id_recommendation PK
        int id_model FK
        int id_area FK
        timestamp recommendation_date
        boolean irrigation_needed
    }

    Irrigation_History {
        int id_irrigation PK
        int id_area FK
        int id_recommendation FK
        timestamp start_time
        timestamp end_time
        float water_volume
    }
```

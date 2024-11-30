import sqlite3

if __name__ == "__main__":
    # Conectar ao banco de dados (ou criar um novo arquivo de banco de dados local)
    conn = sqlite3.connect("src/farmtech.db")
    cursor = conn.cursor()

    # Criar tabela de Área de Plantio
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Area_Plantio (
            id_area INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_area TEXT NOT NULL,
            tamanho_hectares REAL,
            cultura TEXT,
            data_plantio DATE
        );
        """
    )

    # Inserir áreas iniciais de plantio
    cursor.executemany(
        """
        INSERT INTO Area_Plantio (nome_area, tamanho_hectares, cultura, data_plantio)
        VALUES (?, ?, ?, ?)
        """,
        [
            ("Setor A", 10.5, "Milho", "2024-01-15"),
            ("Setor B", 8.2, "Soja", "2024-02-01"),
        ],
    )

    # Criar a tabela Tipo_Sensor
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Tipo_Sensor (
            id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT
        );
        """
    )

    # Criar a tabela Sensor
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Sensor (
            id_sensor INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tipo INTEGER NOT NULL,
            id_area INTEGER NOT NULL,
            nome_sensor TEXT NOT NULL,
            FOREIGN KEY (id_tipo) REFERENCES Tipo_Sensor(id_tipo),
            FOREIGN KEY (id_area) REFERENCES Area_Plantio(id_area)
        );
        """
    )

    # Criar a tabela Medicao_Sensor
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Medicao_Sensor (
            id_medicao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_sensor INTEGER NOT NULL,
            id_area INTEGER NOT NULL,
            valor REAL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            condicoes_ambiente TEXT,
            FOREIGN KEY (id_sensor) REFERENCES Sensor(id_sensor),
            FOREIGN KEY (id_area) REFERENCES Area_Plantio(id_area)
        );
        """
    )

    # Tabela de Modelos de Machine Learning
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Modelo_ML (
            id_modelo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_modelo TEXT NOT NULL,
            tipo_modelo TEXT NOT NULL,  # Classificação, Regressão, etc
            data_treinamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            parametros_modelo TEXT,  # Armazenar hiperparâmetros serializados
            biblioteca_ml TEXT NOT NULL  # Scikit-learn, TensorFlow, etc
        );
        """
    )

    # Tabela de Métricas do Modelo
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Metricas_Modelo (
            id_metrica INTEGER PRIMARY KEY AUTOINCREMENT,
            id_modelo INTEGER,
            metrica TEXT NOT NULL,  # Accuracy, F1-Score, MAE, etc
            valor_metrica REAL,
            FOREIGN KEY (id_modelo) REFERENCES Modelo_ML(id_modelo)
        );
        """
    )

    # Tabela de Recomendação de Irrigação
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Recomendacao_Irrigacao (
            id_recomendacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_modelo INTEGER,
            id_area INTEGER,
            data_recomendacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            necessidade_irrigacao BOOLEAN,
            FOREIGN KEY (id_modelo) REFERENCES Modelo_ML(id_modelo),
            FOREIGN KEY (id_area) REFERENCES Area_Plantio(id_area)
        );
        """
    )

    # Tabela de Histórico de Irrigação
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Historico_Irrigacao (
            id_irrigacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_area INTEGER,
            id_recomendacao INTEGER,
            hora_inicio TIMESTAMP,
            hora_fim TIMESTAMP,
            duracao_minutos REAL,
            volume_agua REAL,
            FOREIGN KEY (id_area) REFERENCES Area_Plantio(id_area),
            FOREIGN KEY (id_recomendacao) REFERENCES Recomendacao_Irrigacao(id_recomendacao)
        );
        """
    )

    # Inserir dados iniciais na tabela Tipo_Sensor
    cursor.executemany(
        """
        INSERT INTO Tipo_Sensor (nome, descricao)
        VALUES (?, ?)
        """,
        [
            ("K", "Sensor para medir o nível de Potássio"),
            ("P", "Sensor para medir o nível de Fósforo"),
            ("pH", "Sensor para medir o nível de pH do solo"),
            ("Umidade", "Sensor para medir a umidade do solo"),
        ],
    )

    # Inserir sensores iniciais na tabela Sensor
    cursor.executemany(
        """
        INSERT INTO Sensor (id_tipo, id_area, nome_sensor)
        VALUES (?, ?, ?)
        """,
        [
            (1, 1, "Sensor K - Setor A"),
            (2, 1, "Sensor P - Setor A"),
            (3, 1, "Sensor pH - Setor A"),
            (4, 1, "Sensor Umidade - Setor A"),
            (1, 2, "Sensor K - Setor B"),
            (2, 2, "Sensor P - Setor B"),
            (3, 2, "Sensor pH - Setor B"),
            (4, 2, "Sensor Umidade - Setor B"),
        ],
    )

    # Salvar as alterações e fechar a conexão
    conn.commit()
    conn.close()

    print("Banco de dados e tabelas criados com sucesso no arquivo farmtech.db")

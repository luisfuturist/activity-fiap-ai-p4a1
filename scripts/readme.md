# FarmTech Database Setup

Este projeto utiliza **Python**, **PostgreSQL** e **SQLAlchemy** para gerenciar a base de dados de monitoramento agrícola. Siga as instruções abaixo para configurar o ambiente e inicializar o banco de dados.

---

## **Índice**
- [Pré-requisitos](#pré-requisitos)
- [Passo 1: Criar e Ativar um Ambiente Virtual](#passo-1-criar-e-ativar-um-ambiente-virtual)
- [Passo 2: Instalar Dependências](#passo-2-instalar-dependências)
- [Passo 3: Configurar e Inicializar o Banco de Dados](#passo-3-configurar-e-inicializar-o-banco-de-dados)
- [Passo 4: Inicializar o Banco de Dados](#passo-4-inicializar-o-banco-de-dados)
- [Modelagem Entidade-Relacionamento (MER)](#modelagem-entidade-relacionamento-mer)
- [Problemas Comuns](#problemas-comuns)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## **Pré-requisitos**

1. **Python 3.8 ou superior**  
   Certifique-se de que o Python está instalado em sua máquina. [Baixe aqui](https://www.python.org/downloads/).

2. **PostgreSQL**  
   Instale o PostgreSQL em sua máquina. [Instruções de instalação](https://www.postgresql.org/download/).

3. **Pip**  
   O `pip` é o gerenciador de pacotes do Python. Ele vem instalado com o Python, mas você pode atualizá-lo com:
   ```bash
   python -m pip install --upgrade pip
   ```

---

## **Passo 1: Criar e Ativar um Ambiente Virtual**

O ambiente virtual (**venv**) isola as dependências do projeto, evitando conflitos com outras aplicações.

### **Criar o ambiente virtual**
```bash
python -m venv venv
```

### **Ativar o ambiente virtual**
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

Se ativado com sucesso, o terminal mostrará o nome do ambiente virtual antes do prompt:
```bash
(venv) $
```

---

## **Passo 2: Instalar Dependências**

Com o ambiente virtual ativado, instale as dependências do projeto listadas no arquivo `requirements.txt`.

### **Instalar as dependências**
```bash
pip install -r requirements.txt
```

### **Arquivo `requirements.txt`**
Certifique-se de que o arquivo contém as bibliotecas necessárias:
```
psycopg2-binary
sqlalchemy
```

---

## **Passo 3: Configurar e Inicializar o Banco de Dados**

### **Configurar o PostgreSQL**
Certifique-se de que o PostgreSQL está em execução e crie um banco de dados chamado `fiap_p4a1`. Você pode usar o cliente de linha de comando `psql` ou uma ferramenta GUI como o **pgAdmin**.

### **Criar o banco de dados**
1. Acesse o PostgreSQL com seu usuário:
   ```bash
   psql -U postgres
   ```
2. Crie o banco de dados:
   ```sql
   CREATE DATABASE fiap_p4a1;
   ```
3. Crie o usuário e configure a senha:
   ```sql
   CREATE USER fiap_p4a1 WITH PASSWORD 'fiap_p4a1';
   GRANT ALL PRIVILEGES ON DATABASE fiap_p4a1 TO fiap_p4a1;
   ```

---

## **Passo 4: Inicializar o Banco de Dados**

Com o PostgreSQL configurado, execute o script Python para criar as tabelas e inserir os dados iniciais.

### **Executar o script**
```bash
python scripts/init_db.py
```

Se tudo ocorrer corretamente, a saída será:
```
Database and tables created, initial data added successfully.
```

---

## Modelagem Entidade-Relacionamento (MER)

Esta é a modelagem das entidades e seus relacionamentos para o banco de dados utilizado no sistema de monitoramento agrícola.

### **Entidades e Relacionamentos**

### **1. `Planting_Area`**
A tabela **`Planting_Area`** representa as áreas de plantio.

**Atributos:**
- `id_area` (PK): Identificador único da área de plantio
- `area_name`: Nome da área
- `size_hectares`: Tamanho da área em hectares
- `crop`: Tipo de cultura
- `planting_date`: Data de plantio

**Relacionamentos:**
- Uma **`Planting_Area`** pode ter várias **`Harvest`**.
- Uma **`Planting_Area`** pode ter vários **`Sensor`**.
- Uma **`Planting_Area`** pode ter várias **`Sensor_Measurement`**.
- Uma **`Planting_Area`** pode ter várias **`Irrigation_Recommendation`**.
- Uma **`Planting_Area`** pode ter várias **`Irrigation_History`**.

---

### **2. `Harvest`**
A tabela **`Harvest`** armazena informações sobre colheitas.

**Atributos:**
- `id_harvest` (PK): Identificador único da colheita
- `id_area` (FK): Referência à área de plantio
- `planting_date`: Data de plantio
- `harvest_date`: Data de colheita
- `emergence_date`: Data de emergência
- `phenological_stage`: Estágio fenológico
- `yield_value`: Valor de produtividade

**Relacionamentos:**
- Uma **`Harvest`** está associada a uma única **`Planting_Area`**.
- Uma **`Harvest`** pode ter várias **`Sensor_Measurement`**.

---

### **3. `Sensor_Type`**
A tabela **`Sensor_Type`** define os tipos de sensores.

**Atributos:**
- `id_type` (PK): Identificador único do tipo de sensor
- `name`: Nome do tipo de sensor
- `description`: Descrição do tipo de sensor

**Relacionamentos:**
- Um **`Sensor_Type`** pode ter vários **`Sensor`**.

---

### **4. `Sensor`**
A tabela **`Sensor`** representa os sensores instalados.

**Atributos:**
- `id_sensor` (PK): Identificador único do sensor
- `id_type` (FK): Referência ao tipo de sensor
- `id_area` (FK): Referência à área de plantio
- `sensor_name`: Nome do sensor

**Relacionamentos:**
- Um **`Sensor`** está associado a um único **`Sensor_Type`**.
- Um **`Sensor`** está associado a uma única **`Planting_Area`**.
- Um **`Sensor`** pode ter várias **`Sensor_Measurement`**.

---

### **5. `Sensor_Measurement`**
A tabela **`Sensor_Measurement`** armazena medições dos sensores.

**Atributos:**
- `id_measurement` (PK): Identificador único da medição
- `id_sensor` (FK): Referência ao sensor
- `id_area` (FK): Referência à área de plantio
- `id_harvest` (FK): Referência opcional à colheita
- `measurement`: Valor da medição
- `datetime`: Data e hora da medição
- `environmental_conditions`: Condições ambientais

**Relacionamentos:**
- Uma **`Sensor_Measurement`** está associada a um único **`Sensor`**.
- Uma **`Sensor_Measurement`** está associada a uma única **`Planting_Area`**.
- Uma **`Sensor_Measurement`** pode estar associada a uma única **`Harvest`**.

---

### **6. `ML_Model`**
A tabela **`ML_Model`** armazena informações sobre modelos de Machine Learning.

**Atributos:**
- `id_model` (PK): Identificador único do modelo
- `model_name`: Nome do modelo
- `model_type`: Tipo do modelo
- `training_date`: Data de treinamento
- `model_parameters`: Parâmetros do modelo
- `ml_library`: Biblioteca de Machine Learning
- `accuracy`: Acurácia do modelo
- `precision`: Precisão do modelo
- `recall`: Recall do modelo
- `f1_score`: Pontuação F1

**Relacionamentos:**
- Um **`ML_Model`** pode ter várias **`Irrigation_Recommendation`**.

---

### **7. `Irrigation_Recommendation`**
A tabela **`Irrigation_Recommendation`** armazena recomendações de irrigação.

**Atributos:**
- `id_recommendation` (PK): Identificador único da recomendação
- `id_model` (FK): Referência ao modelo de Machine Learning
- `id_area` (FK): Referência à área de plantio
- `recommendation_date`: Data da recomendação
- `irrigation_needed`: Indicador de necessidade de irrigação

**Relacionamentos:**
- Uma **`Irrigation_Recommendation`** está associada a um único **`ML_Model`**.
- Uma **`Irrigation_Recommendation`** está associada a uma única **`Planting_Area`**.
- Uma **`Irrigation_Recommendation`** pode ter várias **`Irrigation_History`**.

---

### **8. `Irrigation_History`**
A tabela **`Irrigation_History`** registra o histórico de irrigações.

**Atributos:**
- `id_irrigation` (PK): Identificador único do registro de irrigação
- `id_area` (FK): Referência à área de plantio
- `id_recommendation` (FK): Referência à recomendação de irrigação
- `start_time`: Hora de início da irrigação
- `end_time`: Hora de fim da irrigação
- `water_volume`: Volume de água utilizado

**Relacionamentos:**
- Uma **`Irrigation_History`** está associada a uma única **`Planting_Area`**.
- Uma **`Irrigation_History`** está associada a uma única **`Irrigation_Recommendation`**.


## **Diagrama Entidade-Relacionamento (DER)**
![DER](../assets/DER.png)


## **Problemas Comuns**

### **Ambiente virtual não ativa**
Certifique-se de estar usando a versão correta do Python e o caminho correto para o `venv`.

### **Erro ao conectar ao PostgreSQL**
Verifique se o PostgreSQL está em execução e se o host, usuário e senha estão configurados corretamente no script Python.

---

## **Contribuindo**

Sinta-se à vontade para contribuir com melhorias ou reportar problemas. 

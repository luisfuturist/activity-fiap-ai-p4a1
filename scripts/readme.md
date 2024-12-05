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

## **Configurar o PostgreSQL com Docker**

### **Pré-requisitos**
Certifique-se de que o Docker e o Docker Compose estão instalados em sua máquina.

### **Passo 1: Configurar o arquivo `docker-compose.yaml`**
Crie um arquivo chamado `docker-compose.yaml` com o seguinte conteúdo:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: fiap_p4a1_postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: fiap_p4a1
      POSTGRES_PASSWORD: fiap_p4a1
      POSTGRES_DB: fiap_p4a1
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### **Passo 2: Executar o PostgreSQL**
1. No terminal, navegue até o diretório onde está o arquivo `docker-compose.yaml`.
2. Execute o comando para iniciar o contêiner:
   ```bash
   docker-compose up -d
   ```

   - Isso fará o download da imagem do PostgreSQL (caso ainda não esteja no sistema), configurará o banco de dados e o disponibilizará na porta 5432.

3. Confirme que o contêiner está rodando:
   ```bash
   docker ps
   ```

   Você deverá ver o contêiner `fiap_p4a1_postgres` em execução.

### **Passo 3: Acessar o PostgreSQL**
Caso queira acessar o PostgreSQL no contêiner para verificar a configuração, use:
```bash
docker exec -it fiap_p4a1_postgres psql -U fiap_p4a1 -d fiap_p4a1
```

### **Passo 4: Executar o script Python**
Agora, com o PostgreSQL rodando no Docker, execute o script Python normalmente:
```bash
python scripts/init_db.py
```

Se o script estiver configurado corretamente com `DATABASE_URL`, a saída esperada será:
```
Database populated successfully!
```

---

### **Considerações para o `DATABASE_URL`**
No seu script Python, o valor de `DATABASE_URL` não precisa ser alterado, pois o contêiner expõe o PostgreSQL na porta padrão `5432` no host local.

Se, por algum motivo, o script Python não estiver rodando na mesma máquina que o Docker, ajuste `DATABASE_URL` para usar o IP ou hostname do servidor Docker. Por exemplo:
```
DATABASE_URL="postgresql://fiap_p4a1:fiap_p4a1@<docker_host_ip>:5432/fiap_p4a1"
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


## Exemplo de Operações CRUD

Esta seção demonstra o uso das operações CRUD definidas em `planting_area_crud.py`.  Estas funções agora acessam a sessão de banco de dados diretamente através do arquivo `database_session.py`, simplificando seu uso. A função `update_planting_area` agora utiliza `typing.TypedDict` para tipagem, melhorando a autocompletação no VS Code sem a necessidade de validação em tempo de execução do Pydantic.

As operações CRUD para as entidades `Harvest`, `Sensor`, `Sensor_Measurement`, `ML_Model`, `Irrigation_Recommendation` e `Irrigation_History` podem ser realizadas de forma similar.

**Pré-requisitos:** Certifique-se de que os arquivos `database_session.py` e `planting_area_crud.py` estejam no mesmo diretório. Certifique-se também que o banco de dados PostgreSQL esteja rodando.


Primeiro, certifique-se de ter as seguintes importações no seu arquivo principal (ex: `app.py`):

```python
from .planting_area_crud import (
    create_planting_area,
    get_planting_area,
    get_all_planting_areas,
    update_planting_area,
    delete_planting_area,
)
import datetime
```

Em seguida, use as funções como mostrado neste exemplo (em `app.py` ou similar):


```python
# ... (Outras importações e código, se necessário) ...

# Exemplo de uso com tratamento de erros:

try:
    new_area = create_planting_area("Área B", 12.0, "Trigo", "2024-04-10")
    print(f"Área de plantio criada: {new_area}")

    retrieved_area = get_planting_area(new_area.id_area)
    print(f"Área de plantio recuperada: {retrieved_area}")

    all_areas = get_all_planting_areas()
    print(f"Todas as áreas de plantio: {all_areas}")

    # Atualizando apenas o campo 'crop'
    updated_area = update_planting_area(new_area.id_area, {"crop": "Cevada"})
    print(f"Área de plantio atualizada: {updated_area}")

    deleted = delete_planting_area(new_area.id_area)
    print(f"Área de plantio deletada: {deleted}")

except Exception as e:
    print(f"Ocorreu um erro durante a operação CRUD: {e}")

```

**Observações:**

* A função `update_planting_area` aceita um dicionário como parâmetro, seguindo a definição de tipo `PlantingAreaUpdate` em `planting_area_crud.py`.  Este dicionário pode conter apenas os campos que você deseja atualizar.  A tipagem com `TypedDict` auxilia na autocompletação no VS Code, mas não realiza validação em tempo de execução dos dados. Para validação, considere o uso de Pydantic.
* Certifique-se de que o banco de dados esteja em execução antes de executar este exemplo.
* Substitua "Trigo" e "Cevada" por outros tipos de cultura, se necessário.


## **Problemas Comuns**

### **Ambiente virtual não ativa**
Certifique-se de estar usando a versão correta do Python e o caminho correto para o `venv`.

### **Erro ao conectar ao PostgreSQL**
Verifique se o PostgreSQL está em execução e se o host, usuário e senha estão configurados corretamente no script Python.

---

## **Contribuindo**

Sinta-se à vontade para contribuir com melhorias ou reportar problemas. 

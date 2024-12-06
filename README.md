# activity-fiap-ai-p4a1

> **Note:**  
> This repository is part of the **Artificial Intelligence** course at [FIAP](https://github.com/fiap) - Online 2024. It contains the activity titled *"Chapter 1 - Automation and Intelligence in the FarmTech Solution"* from Phase 4.

This repository provides a solution for optimizing irrigation and nutrient management through predictive intelligence and real-time monitoring. The enhanced system combines Scikit-learn for predictive modeling, Streamlit for interactive dashboards, and ESP32 for field hardware integration. It marks a significant upgrade from previous versions, introducing improvements in database architecture, embedded systems, and a user-friendly interface to deliver actionable insights for smarter farming.

## Features

- **Database**: PostgreSQL database for data persistence and efficient queries.  
- **Interactive Dashboard**: A user-friendly Streamlit app to visualize real-time data.  
- **ESP32 Integration**: Seamless communication with field hardware for data collection and irrigation control.  
- **Predictive Modeling**: Machine learning models built with Scikit-learn to predict irrigation needs. 

### Key Improvements

1. **Database Enhancements**  
   - Transitioned to a more robust **PostgreSQL** database structure to handle data more efficiently.
   - Improved data schema for storing and querying historical data, such as soil moisture and nutrient levels.
   - Enhanced naming conventions for columns and table names.

2. **Streamlit Integration**  
    - Developed a user-friendly **dashboard** using Streamlit to visualize real-time irrigation data.
    - Implemented dynamic charts to monitor soil metrics.
    - Achieved seamless integration with Python to showcase insights from the machine learning model.

3. **ESP32 Enhancements**  
   - Optimized sensor integration and memory usage.
   - Connected ESP32 to a **Wokwi simulation**, which now sends data to the dashboard through an MQTT protocol.

4. **Predictive Modeling with Scikit-learn**  
   - Developed a predictive model to recommend irrigation actions based on historical data.
   - Incorporated machine learning for actionable insights into water management. 

## Installation

Before proceeding, ensure the following prerequisites are installed on your system:

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose)

Additional tools for setup:

- [VS Code](https://code.visualstudio.com/download)
- [Python 3.x](https://www.python.org/)

Consider installing these VS Code extensions:

- [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) (optional)
  - [SQLTools PostgreSQL Driver](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-pg)

To clone the repository to your local machine:

```sh
git clone https://github.com/luisfuturist/activity-fiap-ai-p4a1.git
cd activity-fiap-ai-p4a1/
```

## Setup

1. **Database Setup (PostgreSQL)**:
   - Start the database:
    ```bash
    docker compose up -d
    ```
    - Stop the database:
    ```bash
    docker compose down
    ```

2. **Create and Activate a Virtual Environment**:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Solutions

1. **Running the app**:
   - Start the interface with:
     ```bash
     streamlit run src/streamlit_app.py
     ```

2. **ESP32**:
   - Project link on Wokwi: [Wokwi Project](https://wokwi.com/projects/415998871219053569)
   - Access the code in the `Platformio/` folder.

## Project Management

Access the [GitHub Project](https://github.com/users/luisfuturist/projects/4).

## Members (Group 60)

- [Amandha Nery](https://www.linkedin.com/in/amandhanery/) (RM560030)
- [Bruno Conterato](https://www.linkedin.com/in/brunoconterato/) (RM561048)
- [Gustavo Castro](https://www.linkedin.com/in/gustavo-castro-29a78a2a/) (RM560831)
- [Kild Fernandes](https://www.linkedin.com/in/kild-fernandes/) (RM560615)
- [Luis Emidio](https://www.linkedin.com/in/luisfuturist/) (RM559976)

## Professors

- **Tutor**: [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)
- **Coordinator**: [André Godoi](https://www.linkedin.com/in/profandregodoi/)

## License

This project is licensed under the [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).

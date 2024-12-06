# activity-fiap-ai-p4a1

> **Note:**  
> This project is part of the **Artificial Intelligence** course at [FIAP](https://github.com/fiap) - Online 2024. It is the "**Phase 4** Activity Chapter 1 - Automation and intelligence in the FarmTech solution."

## Overview

### Objective

Develop an enhanced FarmTech solution by integrating predictive intelligence and real-time monitoring to optimize irrigation and nutrient management. Leverage Scikit-learn for predictive modeling, Streamlit for visualization, and ESP32 for field hardware integration.

### **Key Improvements in Phase 4**

1. **Database Enhancements**  
   - Transitioned to a more robust **PostgreSQL** database structure to handle data more efficiently.
   - Improved data schema for storing and querying historical data, such as soil moisture and nutrient levels.
   - Seamless integration with Python for real-time analysis and predictive modeling.

2. **Streamlit Integration**  
   - Built a fully functional, interactive **dashboard** to visualize soil and nutrient data in real-time.
   - Added dynamic charts to monitor metrics, generate insights, and display the results of predictive models.

3. **ESP32 Enhancements**  
   - Optimized sensor integration and memory usage.
   - Connected ESP32 to a **Wokwi simulation**, which now sends data to the dashboard through an MQTT protocol.

4. **Predictive Modeling with Scikit-learn**  
   - Developed a predictive model to recommend irrigation actions based on historical data.
   - Incorporated machine learning for actionable insights into water and nutrient management.

## Features

- **Predictive Modeling**: Advanced machine learning models built with Scikit-learn to predict irrigation needs.  
- **Interactive Dashboard**: A user-friendly Streamlit app to visualize real-time data.  
- **ESP32 Integration**: Seamless communication with field hardware for data collection and irrigation control.  
- **Database Integration**: Enhanced PostgreSQL database for data persistence and efficient queries.  

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
cd activity-fiap-ai-p4a3/
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

2. **Create and Activate Virtual Environment**:
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
- Gustavo Castro (RM560831)
- [Kild Fernandes](https://www.linkedin.com/in/kild-fernandes/) (RM560615)
- [Luis Emidio](https://www.linkedin.com/in/luisfuturist/) (RM559976)

## Professors

- **Tutor**: [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)
- **Coordinator**: [André Godoi](https://www.linkedin.com/in/profandregodoi/)

## License

This project is licensed under the [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).

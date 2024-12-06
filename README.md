# activity-fiap-ai-p4a1

> **Note:**  
> This repository is part of the **Artificial Intelligence** course at [FIAP](https://github.com/fiap) - Online 2024. It contains the activity titled *"Chapter 1 - Automation and Intelligence in the FarmTech Solution"* from Phase 4.

This repository contains a solution for optimizing irrigation and nutrient management through predictive intelligence and real-time monitoring. It incorporates Scikit-learn for predictive modeling, Streamlit for interactive dashboards, and ESP32 for field hardware integration. Enhancements include a refined database architecture, embedded systems optimization, and an intuitive user interface for smarter farming.

## Features

- **Database**: PostgreSQL for efficient data storage and querying.  
- **Interactive Dashboard**: Real-time data visualization with Streamlit.  
- **ESP32 Integration**: Communication with field hardware for data collection and irrigation control.  
- **Predictive Modeling**: Machine learning models using Scikit-learn for irrigation recommendations.

### Key Improvements

### 1. **Database Enhancements**  
   - Transitioned to **PostgreSQL** for improved data handling.  
   - Revised schema to store historical data like soil moisture and nutrient levels.  
   - Standardized column and table naming conventions.  

### 2. **Streamlit Dashboard**  
   - Enhanced interactivity and data visualization.  
   - Dynamic charts for real-time monitoring of soil metrics.  
   - Integrated insights from machine learning models.

### 3. **ESP32 and Hardware Integration**  
   - Optimized sensor integration and memory usage.  
   - Connected ESP32 to a **Wokwi simulation** for real-time data transmission via MQTT.  
   - Added an LCD display (I2C protocol) to show critical metrics (e.g., soil moisture, nutrient levels).  
   - Implemented real-time monitoring with Serial Plotter for variable tracking.  

### 4. **Predictive Modeling**  
   - Created a predictive irrigation model using Scikit-learn.  
   - Recommendations based on historical soil and nutrient data.  
   - Enabled actionable insights for efficient water management.

## Demonstrations and Evidence

### **Serial Plotter Integration**  
Below are screenshots of the Serial Plotter showcasing variable tracking (e.g., soil moisture) in real time:

![Serial Plotter Example](path/to/serial_plotter_image.png)  
*Description: The Serial Plotter graph shows changes in soil moisture over time, helping visualize irrigation needs.*

### **Video Demonstration**  
A demonstration video showing the updated system in action is available on YouTube (unlisted): [Watch the Video](https://youtube.com/your-video-link)

## Installation

### Prerequisites

Ensure the following tools are installed on your system:

- [Git](https://git-scm.com/downloads)  
- [Docker](https://docs.docker.com/)  
- [Docker Compose](https://docs.docker.com/compose/)  
- [Python 3.x](https://www.python.org/)  
- [VS Code](https://code.visualstudio.com/download) (Optional: [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools))  

### Clone the Repository

```bash
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

## Running the Solutions

### 1. **Application**  
   Start the app:
   ```bash
   streamlit run src/streamlit_app.py
   ```

### 2. **ESP32 Integration**  
   - Access the Wokwi project: [Wokwi Project](https://wokwi.com/projects/415998871219053569)  
   - The ESP32 code is located in the `Platformio/` folder.  
   - Metrics are displayed on the LCD screen, and Serial Plotter monitors real-time variable changes.

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

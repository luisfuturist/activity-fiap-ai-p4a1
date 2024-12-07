# Smart Agriculture System with Wokwi

## Overview
This project implements a **Smart Agriculture Monitoring and Control System** using an ESP32 microcontroller, multiplexers, and sensors. It collects data such as temperature, humidity, soil moisture, and nutrient levels. The system also incorporates an LCD for real-time data display, MQTT for remote monitoring, and LEDs for visual feedback. The circuit is designed and simulated using **Wokwi**.

---

## Features
- **Data Collection**:
  - Temperature and humidity sensing using DHT22.
  - Soil moisture and nutrient monitoring using multiplexers.
- **Data Display**:
  - Real-time display of sensor readings on a 20x4 I2C LCD.
- **Data Communication**:
  - Publishes sensor data to MQTT channels.
  - Supports remote monitoring through an MQTT broker.
- **Visual Feedback**:
  - LEDs controlled via shift registers to indicate channel states.
- **Automation**:
  - Regularly reads sensor data and updates outputs.
  - Manages irrigation and channel states dynamically.

---

## Hardware Components
### Microcontroller
- **ESP32**: The main processing unit for managing sensors, communication, and logic.

### Sensors
- **DHT22**: Measures temperature and humidity.
- **Soil Moisture Sensors**: Measure soil water content.
- **Nutrient Sensors**: Monitor nutrient levels in the soil.

### Display
- **20x4 I2C LCD**: Displays sensor readings and system information.

### Multiplexers
- **CD74HC4067**: Expands ESP32's analog inputs to handle multiple sensors.

### Shift Register
- **74HC595**: Controls LEDs for channel state representation.

### LEDs
- Provide visual feedback for channel states (e.g., irrigation activity).

---

## Software Components
### Libraries
- **Arduino Core**: Fundamental support for ESP32 programming.
- **ArduinoJson**: JSON serialization for MQTT data payloads.
- **LiquidCrystal_I2C**: Controls the I2C LCD.
- **PubSubClient**: Implements MQTT client functionality.
- **WiFi**: Manages Wi-Fi connectivity for the ESP32.
- **DHT**: Integrates temperature and humidity sensor.

---

## System Logic

### Setup Phase
- Initializes components like LCD, multiplexers, Wi-Fi, and MQTT client.

### Main Loop
- Periodically:
  - Reads sensor data.
  - Publishes data to MQTT topics.
  - Updates LED states and displays data on the LCD.

### Sensor Data Processing
- Reads data from DHT22, soil moisture, and nutrient sensors.
- Converts raw sensor values into meaningful percentages or units.

### Data Publishing
- Formats data into JSON objects and publishes to MQTT channels.

### Shift Register Control
- Manages LED states using the 74HC595 shift register.

---

## MQTT Topics
- **Sensor Data Channels**:
  - `chanel/c0`, `chanel/c1`, ..., `chanel/c15`: Publish soil and nutrient sensor data.
- **Irrigation Channels**:
  - `irrigation/c0`, ..., `irrigation/c15`: Manage irrigation states.
- **LED Control Topics**:
  - `led/c0`, ..., `led/c3`: Control channel states remotely.

---

## Circuit Diagram
The circuit includes:
- ESP32 microcontroller connected to sensors and peripherals.
- Multiplexers for handling multiple sensors.
- LCD for real-time display.
- Shift registers and LEDs for channel feedback.

---

## Key Functions
### `setup()`
- Initializes all components and establishes Wi-Fi and MQTT connections.

### `loop()`
- Regularly reads sensor data, publishes it, and updates outputs.

### `readMux(channel)`
- Reads data from the specified multiplexer channel.

### `initializeLCD()`
- Configures the LCD for I2C communication and displays initial messages.

### `connectToWiFi()`
- Connects the ESP32 to the specified Wi-Fi network.

### `connectMQTT()`
- Establishes a connection to the MQTT broker and subscribes to topics.

### `EnviaValores()`
- Formats and sends sensor data to MQTT topics in JSON format.

### `updateShiftRegister()`
- Updates LED states using the shift register.

---

## Simulation
### Platform
- Designed and simulated on **Wokwi**.

### Simulation Features
- Displays sensor readings and channel states.
- Simulates MQTT communication for remote monitoring.

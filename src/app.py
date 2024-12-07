import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime
import time
import os
from filelock import FileLock

# Global DataFrame to store MQTT messages
mqtt_data = pd.DataFrame(columns=["chanel", "potassiumPercent", "phosphorusPercent", "temperature", "humidity", "irrigation", "timestamp"])

# MQTT Credentials
MQTT_BROKER = "759d2f782c6f48d68eafab33492641f8.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "sla"
MQTT_PASSWORD = "sla"

# CSV file name and lock file
CSV_FILE = "mqtt_data.csv"
LOCK_FILE = CSV_FILE + ".lock"

# Function to save DataFrame to CSV
def save_to_csv():
    with FileLock(LOCK_FILE):
        mqtt_data.to_csv(CSV_FILE, index=False)
    print(f"Dados atualizados salvos em {CSV_FILE}")

# Function to load data from CSV
def load_from_csv():
    global mqtt_data
    with FileLock(LOCK_FILE):
        if os.path.exists(CSV_FILE):
            mqtt_data = pd.read_csv(CSV_FILE)
    print("Dados carregados do CSV")

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully to MQTT broker with result code {rc}")
        client.subscribe("chanel/#")  # Subscribe to the topic
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global mqtt_data
    payload = msg.payload.decode()
    print(f"Dados recebidos do tópico {msg.topic}: {payload}")
   
    try:
        # Parse JSON payload
        data = json.loads(payload)
        data["chanel"] = msg.topic  # Add channel name
        data["timestamp"] = datetime.now()  # Add timestamp
       
        # Create a new DataFrame with the latest data
        new_data = pd.DataFrame([data])
       
        # Update the mqtt_data DataFrame
        with FileLock(LOCK_FILE):
            mqtt_data = pd.concat([mqtt_data, new_data]).drop_duplicates(subset="chanel", keep="last").reset_index(drop=True)
       
        # Print the updated DataFrame
        print("\nDataFrame atualizado:")
        print(mqtt_data)

        # Save to CSV after each update
        save_to_csv()
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {payload}")

# Setup MQTT Client
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)  # Set username and password
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()  # Enable TLS for secure communication
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Load existing data from CSV before starting
load_from_csv()

client.loop_start()

print("Script iniciado. Aguardando mensagens MQTT...")
try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    print("\nScript encerrado pelo usuário.")
    save_to_csv()  # Final save before exiting
    client.loop_stop()
    client.disconnect()
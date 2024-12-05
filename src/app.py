import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime
import time

# Global DataFrame to store MQTT messages
mqtt_data = pd.DataFrame(columns=["chanel", "soilMoisture", "nutrientLevel", "temperature", "humidity", "irigation", "timestamp"])

# MQTT Credentials
MQTT_BROKER = "759d2f782c6f48d68eafab33492641f8.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "sla"
MQTT_PASSWORD = "sla"

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
        
        # Append to DataFrame
        mqtt_data = pd.concat([mqtt_data, pd.DataFrame([data])], ignore_index=True)
        
        # Print the updated DataFrame
        print("\nDataFrame atualizado:")
        print(mqtt_data)
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {payload}")

# Setup MQTT Client
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)  # Set username and password
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()  # Enable TLS for secure communication
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

if __name__ == '__main__':
    print("Script iniciado. Aguardando mensagens MQTT...")
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("\nScript encerrado pelo usuário.")
        client.loop_stop()
        client.disconnect()

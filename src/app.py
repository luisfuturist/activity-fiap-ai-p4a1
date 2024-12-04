import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime

# Global DataFrame to store MQTT messages
mqtt_data = pd.DataFrame(columns=["chanel", "soilMoisture", "nutrientLevel", "temperature", "humidity", "irigation", "timestamp"])

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com o código de resultado {rc}")
    client.subscribe("chanel/#")


def on_message(client, userdata, msg):
    global mqtt_data
    payload = msg.payload.decode()
    print(f"Dados recebidos do tópico {msg.topic}: {payload}")
    
    try:
        # Parse JSON payload
        data = json.loads(payload)
        data["chanel"] = msg.topic  # Add a timestamp for each message
        data["timestamp"] = datetime.now()  # Add a timestamp for each message
        
        # Append to DataFrame
        mqtt_data = pd.concat([mqtt_data, pd.DataFrame([data])], ignore_index=True)
        
        # Print the updated DataFrame
        print("\nDataFrame atualizado:")
        print(mqtt_data)
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON: {payload}")


# Setup MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("ed2ea25756ed469286b02eab0afe20cf.s1.eu.hivemq.cloud", 1883, 60)
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
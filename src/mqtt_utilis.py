import paho.mqtt.client as mqtt
import json
import time

# MQTT Credentials
MQTT_BROKER = "759d2f782c6f48d68eafab33492641f8.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "sla"
MQTT_PASSWORD = "sla"

def activate_irrigation(channel, broker=MQTT_BROKER, port=MQTT_PORT, username=MQTT_USER, password=MQTT_PASSWORD):
    result_message = ""

    def on_connect(client, userdata, flags, rc):
        nonlocal result_message
        if rc == 0:
            print(f"Connected successfully to MQTT broker with result code {rc}")
            # Publish the irrigation activation message
            message = json.dumps(true)
            client.publish(f"led/{channel}", message)
            result_message = f"Irrigation activation message sent to {channel}"
        else:
            result_message = f"Failed to connect, return code {rc}"

    def on_publish(client, userdata, mid):
        nonlocal result_message
        result_message += "\nMessage published successfully"
        print("Message published successfully")
        client.disconnect()

    # Setup MQTT Client
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.tls_set()  # Enable TLS for secure communication

    try:
        client.connect(broker, port, 60)
        client.loop_start()
        time.sleep(2)  # Wait for the message to be published
        client.loop_stop()
    except Exception as e:
        result_message = f"Error: {str(e)}"

    return result_message

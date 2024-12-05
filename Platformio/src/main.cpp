#include "main.h"

// LCD instance
DHT dht22(DHT_COM_PIN, DHT_MODEL);
LiquidCrystal_I2C lcd(0x27, 20, 4);

// MQTT client
WiFiClientSecure secureClient;
PubSubClient client(secureClient);

// Define mux_channels array
const char* mux_channels[] = {
    "chanel/c0", "chanel/c1", "chanel/c2", "chanel/c3",
    "chanel/c4", "chanel/c5", "chanel/c6", "chanel/c7",
    "chanel/c8", "chanel/c9", "chanel/c10", "chanel/c11",
    "chanel/c12", "chanel/c13", "chanel/c14", "chanel/c15"
};

const char* irrigation_channels[] = {
    "irrigation/c0", "irrigation/c1", "irrigation/c2", "irrigation/c3",
    "irrigation/c4", "irrigation/c5", "irrigation/c6", "irrigation/c7",
    "irrigation/c8", "irrigation/c9", "irrigation/c10", "irrigation/c11",
    "irrigation/c12", "irrigation/c13", "irrigation/c14", "irrigation/c15"
};

const char* topics[] = { "led/c0", "led/c1", "led/c2", "led/c3" };
bool channelStates[4] = {false, false, false, false}; // Tracks the state of each channel
bool LEDS_STATES[4] = {true, true, true, true}; // Tracks the state of each channel

const uint8_t controlPins[] = {MUX_S0_PIN, MUX_S1_PIN, MUX_S2_PIN, MUX_S3_PIN};

unsigned long lastReadTime = 0;
const unsigned long readInterval = 6000; // 1 minute in milliseconds

void setup() {
  Serial.begin(115200);

  // Initialize LCD
  initializeLCD();

  // Initialize shift register outputs to 0
  updateShiftRegister();

  // Connect to Wi-Fi
  connectToWiFi();

  // Configure MUX control pins as outputs
  for (int i = 0; i < 4; ++i) {
    pinMode(controlPins[i], OUTPUT);
    digitalWrite(controlPins[i], LOW); // Ensure all control pins are LOW initially
  }

  // Configure MUX output pins as inputs (DHT, Soil, Nutrient)
  pinMode(DHT_COM_PIN, INPUT);        
  pinMode(SOIL_COM_PIN, INPUT);        
  pinMode(NUTRIENT_COM_PIN, INPUT);    

   // Initialize shift register control pins
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(latchPin, OUTPUT);

  // Configure MQTT client
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqttCallback); // Set the MQTT callback function
  connectMQTT();

  Serial.println("Setup complete");
}

void loop() {
  client.loop();

  // Update the shift register
  updateShiftRegister();

  delay(100);

  unsigned long currentMillis = millis();
  if (currentMillis - lastReadTime >= readInterval) {
    sendInvertedChannelStates();
    lastReadTime = currentMillis;

    // Read and publish data for all sensors
    readAndPublishAllSensors();
  }
}

void updateShiftRegister() {
  uint8_t ledStates = 0;
  for (uint8_t i = 0; i < 4; i++) {
    if (channelStates[i]) {
      ledStates |= (1 << i); // Set bit i if channelStates[i] is true
    }
  }
  // Invert the bits because HIGH turns the LED ON via the transistor

  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, ledStates);
  digitalWrite(latchPin, HIGH);
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0'; // Null-terminate the payload
  String message = String((char*)payload);

  Serial.printf("Received message on topic %s: %s\n", topic, message.c_str());

  // Find the channel based on the topic
  bool topicMatched = false;
  for (uint8_t i = 0; i < 4; i++) {
    if (String(topic) == String(topics[i])) {
      topicMatched = true;
      if (message.equalsIgnoreCase("true")) {
        channelStates[i] = true;  // Turn ON the corresponding channel
        Serial.printf("Channel %d set to ON\n", i);
      } else if (message.equalsIgnoreCase("false")) {
        channelStates[i] = false; // Turn OFF the corresponding channel
        Serial.printf("Channel %d set to OFF\n", i);
      } else {
        Serial.printf("Invalid message for channel %d. Expected 'true' or 'false'.\n", i);
      }
      break;
    }
  }
  if (!topicMatched) {
    Serial.println("Received message on unknown topic.");
  }
}

void sendInvertedChannelStates() {
  for (uint8_t i = 0; i < 4; i++) {
    // Invert the current state
    LEDS_STATES[i] = !channelStates[i];

    // Create a JSON payload to publish
    DynamicJsonDocument doc(64);
    doc["state"] = LEDS_STATES[i] ? "OFF" : "ON"; // Send "OFF" for true and "ON" for false

    // Serialize JSON to a string
    char jsonBuffer[64];
    serializeJson(doc, jsonBuffer);

    // Publish to the corresponding topic
    if (client.publish(irrigation_channels[i], jsonBuffer)) {
      Serial.printf("Send state of channel %d to topic %s\n", i, topics[i]);
    }
  }
}

void readAndPublishAllSensors() {
  for (int i = 0; i < 16; ++i) {
    readMux(i);
  }
}

void readMux(int channel) {
  for (int i = 0; i < 4; i++) {
    digitalWrite(controlPins[i], (channel >> i) & 1);
  }

  delay(10); // Ensure stable reading

  int soilValue = calculatePercent(analogRead(SOIL_COM_PIN));
  int nutrientValue = calculatePercent(analogRead(NUTRIENT_COM_PIN));

  float humidity = dht22.readHumidity();
  float temperature = dht22.readTemperature();

  if (soilValue != 0.00 || nutrientValue != 0.00) {
    // Display values on LCD
    displayReadingsOnLCD(channel, soilValue, nutrientValue, temperature, humidity);
    logToSerial(soilValue, nutrientValue, temperature, humidity);

    // Send values via MQTT
    EnviaValores(soilValue, nutrientValue, temperature, humidity, mux_channels[channel]);
  }
}

void initializeLCD() {
  Wire.begin(SDA_PIN, SCL_PIN); // Initialize I2C communication
  lcd.init();                   // Initialize the LCD
  lcd.backlight();              // Turn on the backlight
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");
  delay(2000);
  lcd.clear();
}

void EnviaValores(float potassiumPercent, float phosphorusPercent, float temperatura, float umidade, const char* topic) {
  DynamicJsonDocument doc(256); // Use DynamicJsonDocument for simplicity

  doc["soilMoisture"] = potassiumPercent;
  doc["nutrientLevel"] = phosphorusPercent;
  doc["temperature"] = temperatura;
  doc["humidity"] = umidade;

  char jsonBuffer[256];
  serializeJson(doc, jsonBuffer);

  client.publish(topic, jsonBuffer);
  
}

void connectToWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi!");
}

void connectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    secureClient.setInsecure();
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Connected to MQTT broker!");
      for (uint8_t i = 0; i < 4; i++) {
        client.subscribe(topics[i]);
        Serial.printf("Subscribed to topic: %s\n", topics[i]);
      }
    } else {
      Serial.print("Failed to connect, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}




uint8_t calculatePercent(uint16_t value) {
  return map(value, 0, 4095, 0, 100);
}

void logToSerial(float potassiumPercent, float phosphorusPercent, float temperatura, float umidade) {
  Serial.print("Temp: ");
  Serial.print(temperatura);
  Serial.print(" Umid: ");
  Serial.print(umidade);
  Serial.print(" Potassium: ");
  Serial.print(potassiumPercent);
  Serial.print(" Phosphorus: ");
  Serial.println(phosphorusPercent);
}

void displayReadingsOnLCD(int channel, float potassiumPercent, float phosphorusPercent, float temperature, float humidity) {
  lcd.clear(); // Clear the LCD screen

  // Display the channel number on the first line
  lcd.setCursor(0, 0);
  lcd.print("Ch: ");
  lcd.print(channel);
  
  // Display temperature and humidity on the first line
  lcd.setCursor(8, 0); // Move to column 8 for compact display
  lcd.print("Temp: ");
  lcd.print(temperature, 1); // Show temperature with 1 decimal place
  lcd.print("C");

  // Display humidity on the second line
  lcd.setCursor(0, 1);
  lcd.print("Hum: ");
  lcd.print(humidity, 1); // Show humidity with 1 decimal place
  lcd.print("%");

  // Display soil moisture and nutrient level on the third and fourth lines
  lcd.setCursor(0, 2);
  lcd.print("Soil: ");
  lcd.print(potassiumPercent);
  lcd.print("%");

  lcd.setCursor(0, 3);
  lcd.print("Nutri: ");
  lcd.print(phosphorusPercent);
  lcd.print("%");
}


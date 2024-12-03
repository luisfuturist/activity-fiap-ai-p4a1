#include "main.h"

// Instância do LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);

// MQTT client
WiFiClientSecure secureClient;
PubSubClient client(secureClient);

void setup() {
  Serial.begin(115200);

  // Inicializar o LCD
  initializeLCD();

  // Conectar ao Wi-Fi
  connectToWiFi();

  // Conectar ao broker MQTT

  // Configuração do LED de irrigação
  pinMode(IRRIGATION_LED_PIN, OUTPUT);
  digitalWrite(IRRIGATION_LED_PIN, LOW);

  // Configurar cliente seguro

  // Configurar cliente MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqttCallback);
  connectMQTT();

  // Mensagem inicial no monitor serial
  Serial.println("SoilMoisture NutrientLevel IrrigationStatus");
}

void loop() {
  uint16_t soilMoisture = 0, nutrientLevel = 0;
  uint8_t soilMoisturePercent = 0, nutrientLevelPercent = 0;

  client.loop();

  // Ler os sensores
  readSensors(soilMoisture, nutrientLevel);

  // Calcular os valores normalizados
  soilMoisturePercent = calculatePercent(soilMoisture);
  nutrientLevelPercent = calculatePercent(nutrientLevel);

  // Atualizar o status de irrigação
  updateIrrigationStatus(soilMoisturePercent, irrigationStatus);

  // Atualizar o LCD
  displayOnLCD(soilMoisturePercent, nutrientLevelPercent, irrigationStatus);

  // Registrar no monitor serial
  logToSerial(soilMoisturePercent, nutrientLevelPercent, irrigationStatus);

  delay(1000); // Atualizar a cada segundo
}

void connectToWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.print("Conectando-se na rede: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado ao Wi-Fi!");
}

void connectMQTT() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao MQTT...");
    secureClient.setInsecure();
    if (client.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("Conectado ao broker MQTT!");
      client.subscribe(irrigation);
    } else {
      Serial.print("Falha na conexão, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}

// Handle MQTT messages
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Mensagem recebida no tópico ");
    String message;
    for (unsigned int i = 0; i < length; i++) {
        message += (char)payload[i];
    }

    Serial.print("Mensagem recebida no tópico ");
    Serial.print(topic);
    Serial.print(": ");
    Serial.println(message);

    if (String(topic) == irrigation) {
        irrigationStatus = (message == "true");
    } else {
      irrigationStatus = false;
    }
}

// Função para inicializar o LCD
void initializeLCD() {
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");
  delay(2000);
  lcd.clear();
}

// Função para ler os sensores
void readSensors(uint16_t& soilMoisture, uint16_t& nutrientLevel) {
  soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  nutrientLevel = analogRead(NUTRIENT_LEVEL_PIN);
}

// Função para calcular porcentagem (0-100%)
uint8_t calculatePercent(uint16_t value) {
  return map(value, 0, 4095, 0, 100);
}

// Função para atualizar o status de irrigação
void updateIrrigationStatus(uint8_t soilMoisturePercent, bool& irrigationStatus) {
  digitalWrite(IRRIGATION_LED_PIN, irrigationStatus ? HIGH : LOW);
}

// Função para exibir no LCD
void displayOnLCD(uint8_t soilMoisturePercent, uint8_t nutrientLevelPercent, bool irrigationStatus) {
  lcd.setCursor(0, 0);
  lcd.print("Soil: ");
  lcd.print(soilMoisturePercent);
  lcd.print("%    ");

  lcd.setCursor(0, 1);
  lcd.print("Nutrient: ");
  lcd.print(nutrientLevelPercent);
  lcd.print("%   ");

  lcd.setCursor(0, 2);
  lcd.print("Irrigation: ");
  lcd.print(irrigationStatus ? "ON " : "OFF");
}

// Função para registrar no monitor serial
void logToSerial(uint8_t soilMoisturePercent, uint8_t nutrientLevelPercent, bool irrigationStatus) {
  Serial.print(soilMoisturePercent);
  Serial.print(" ");
  Serial.print(nutrientLevelPercent);
  Serial.print(" ");
  Serial.println(irrigationStatus ? 100 : 0);
}

#ifndef MAIN_H
#define MAIN_H

#include <Arduino.h>
#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// MQTT broker configuration
const char* mqtt_server = "759d2f782c6f48d68eafab33492641f8.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_user = "sla";
const char* mqtt_password = "sla";
bool irrigationStatus = false;

// MQTT topics
const char* irrigation = "consumer/irrigation"; 

// Declare mux_channels as external
extern const char* mux_channels[];
extern const uint8_t controlPins[];

// I2C pins for the LCD
#define SDA_PIN 21
#define SCL_PIN 22

// Multiplexer control pins
#define MUX_S0_PIN 12
#define MUX_S1_PIN 13
#define MUX_S2_PIN 14
#define MUX_S3_PIN 15

// Multiplexer output pins
#define DHT_MODEL DHT22
#define DHT_COM_PIN 4  // MUX output 1
#define SOIL_COM_PIN 35  // MUX output 2
#define NUTRIENT_COM_PIN 32  // MUX output 3

// Shift register pins
const int dataPin = 23;   // DS
const int clockPin = 18;  // SHCP
const int latchPin = 5;   // STCP

// Global variables
extern DHT dht22;
extern LiquidCrystal_I2C lcd;

// Function declarations
void initializeLCD();
uint8_t calculatePercent(uint16_t value);
void displayOnLCD(float soilMoisturePercent, float nutrientLevelPercent, float temperatura, float umidade);
void logToSerial(float soilMoisturePercent, float nutrientLevelPercent, float temperatura, float umidade);
void connectToWiFi();
void connectMQTT();
void mqttCallback(char* topic, byte* payload, unsigned int length);
void updateShiftRegister();
void readMux(int channel);
void readAndPublishAllSensors();
void EnviaValores(float soilMoisturePercent, float nutrientLevelPercent, float temperatura, float umidade, const char* topic);
void displayReadingsOnLCD(int channel, float soilMoisturePercent, float nutrientLevelPercent, float temperature, float humidity);

#endif // MAIN_H

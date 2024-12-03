#ifndef MAIN_H
#define MAIN_H

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

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

// Definições de pinos
#define SOIL_MOISTURE_PIN 34  // Pino analógico para umidade do solo
#define NUTRIENT_LEVEL_PIN 35 // Pino analógico para níveis de nutrientes
#define IRRIGATION_LED_PIN 2  // Pino digital para status de irrigação (LED)
#define SDA_PIN 21            // Pino SDA do I2C
#define SCL_PIN 22            // Pino SCL do I2C

// Variáveis globais
extern LiquidCrystal_I2C lcd;

// Declarações de funções
void initializeLCD();
void readSensors(uint16_t& soilMoisture, uint16_t& nutrientLevel);
uint8_t calculatePercent(uint16_t value);
void updateIrrigationStatus(uint8_t soilMoisturePercent, bool& irrigationStatus);
void displayOnLCD(uint8_t soilMoisturePercent, uint8_t nutrientLevelPercent, bool irrigationStatus);
void logToSerial(uint8_t soilMoisturePercent, uint8_t nutrientLevelPercent, bool irrigationStatus);
void mqttCallback(char* topic, byte* payload, unsigned int length);
void connectToWiFi();
void connectMQTT();
void mqttCallback(char* topic, byte* payload, unsigned int length);


#endif // MAIN_H

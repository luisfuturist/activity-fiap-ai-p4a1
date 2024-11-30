#ifndef MAIN_H
#define MAIN_H

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

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

#endif // MAIN_H

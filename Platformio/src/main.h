#ifndef MAIN_H
#define MAIN_H

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

// Pin definitions
#define SOIL_MOISTURE_PIN 34  // Analog pin for soil moisture
#define NUTRIENT_LEVEL_PIN 35 // Analog pin for nutrient levels
#define IRRIGATION_LED_PIN 2  // Digital pin for irrigation status (LED)
#define SDA_PIN 21            // SDA pin for I2C
#define SCL_PIN 22            // SCL pin for I2C

// LCD instance
extern LiquidCrystal_I2C lcd;

// Function prototypes
void initializeLCD();
void readSensors(int &soilMoisture, int &nutrientLevel);
int calculatePercent(int value);
void updateIrrigationStatus(int soilMoisturePercent, bool &irrigationStatus);
void displayOnLCD(int soilMoisturePercent, int nutrientLevelPercent, bool irrigationStatus);
void logToSerial(int soilMoisturePercent, int nutrientLevelPercent, bool irrigationStatus);

#endif // MAIN_H

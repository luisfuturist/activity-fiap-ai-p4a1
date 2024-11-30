#include "main.h"

// Instantiate the LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);

  // Initialize LCD
  initializeLCD();

  // Configure irrigation LED
  pinMode(IRRIGATION_LED_PIN, OUTPUT);
  digitalWrite(IRRIGATION_LED_PIN, LOW);

  // Indicate start in Serial Monitor
  Serial.println("SoilMoisture NutrientLevel IrrigationStatus");
}

void loop() {
  int soilMoisture = 0, nutrientLevel = 0;
  int soilMoisturePercent = 0, nutrientLevelPercent = 0;
  bool irrigationStatus = false;

  // Read sensor values
  readSensors(soilMoisture, nutrientLevel);

  // Calculate percentages
  soilMoisturePercent = calculatePercent(soilMoisture);
  nutrientLevelPercent = calculatePercent(nutrientLevel);

  // Update irrigation status
  updateIrrigationStatus(soilMoisturePercent, irrigationStatus);

  // Display values on LCD
  displayOnLCD(soilMoisturePercent, nutrientLevelPercent, irrigationStatus);

  // Log values to Serial Monitor
  logToSerial(soilMoisturePercent, nutrientLevelPercent, irrigationStatus);

  delay(1000); // Update every second
}

// Initialize the LCD
void initializeLCD() {
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Initializing...");
  delay(2000);
  lcd.clear();
}

// Read sensor values
void readSensors(int &soilMoisture, int &nutrientLevel) {
  soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  nutrientLevel = analogRead(NUTRIENT_LEVEL_PIN);
}

// Calculate percentage (0-100%)
int calculatePercent(int value) {
  return map(value, 0, 4095, 0, 100);
}

// Update irrigation status
void updateIrrigationStatus(int soilMoisturePercent, bool &irrigationStatus) {
  irrigationStatus = soilMoisturePercent < 30; // Example threshold
  digitalWrite(IRRIGATION_LED_PIN, irrigationStatus ? HIGH : LOW);
}

// Display values on LCD
void displayOnLCD(int soilMoisturePercent, int nutrientLevelPercent, bool irrigationStatus) {
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

// Log values to Serial Monitor
void logToSerial(int soilMoisturePercent, int nutrientLevelPercent, bool irrigationStatus) {
  Serial.print(soilMoisturePercent);
  Serial.print(" ");
  Serial.print(nutrientLevelPercent);
  Serial.print(" ");
  Serial.println(irrigationStatus ? 100 : 0);
}

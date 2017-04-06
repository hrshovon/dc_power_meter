#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_INA219.h>

// If using software SPI (the default case):
#define OLED_DC     6
#define OLED_CS     7
#define OLED_RESET  8
Adafruit_SSD1306 oled_handler(OLED_DC, OLED_RESET, OLED_CS);

Adafruit_INA219 pm_handler;

//Voltage,Current and Power unit variables
String i_unit;
String p_unit;

//misc global vars
uint8_t counter=0;

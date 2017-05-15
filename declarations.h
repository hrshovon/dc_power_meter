#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_INA219.h>
#include <TimerOne.h>

#define UPDATE_INTERVAL_US 50000

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
volatile bool update_disp=false;
volatile uint8_t counter=0;
volatile float V,I,P;

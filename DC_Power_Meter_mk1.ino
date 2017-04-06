#include "declarations.h"

void setup() {
  //initialize everything
  //first,display
  Serial.begin(9600);
  init_display();
  //second,the INA219 module
  pm_handler.begin();
  /*
  at this moment,INA219 will run with 32V,2A calibration
  This is because,it should initialize and keep running
  at highest possible sale to keep things safe 
  */
}


void loop() {
  //get,voltage,current and power and dump them all in the display
  
  float V=get_voltage();
  float I=get_current();
  float P=get_power();

  //oled_handler.setTextSize(1);
  //oled_handler.setTextColor(WHITE);
  if(counter==4)
  {
  counter=0;
  oled_handler.clearDisplay();
  oled_handler.setCursor(0,0);
  oled_handler.print("V: ");
  oled_handler.print(V);
  oled_handler.println("V");

  oled_handler.setCursor(0,10);
  oled_handler.print("I: ");
  oled_handler.print(I);
  oled_handler.println(i_unit);

  oled_handler.setCursor(0,20);
  oled_handler.print("P: ");
  oled_handler.print(P);
  oled_handler.println(p_unit);
  
  oled_handler.display();
  }
  else
  {
    counter++;
  }
  send_data_serial(V,I,P);
  delay(100);
}

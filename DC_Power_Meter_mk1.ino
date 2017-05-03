#include "declarations.h"


void update_data()
{
  if(counter==8)
  {
    update_disp=true;
    counter=0;
  }
  else
  {
    counter++;
  }
  send_data_serial(V,I,P);
}
void setup() {
  //initialize everything
  //first,display
  Serial.begin(9600);
  init_display();
  
  //second,the INA219 module
  pm_handler.begin();
  Timer1.initialize(UPDATE_INTERVAL_US);
  Timer1.attachInterrupt(update_data);
  /*
  at this moment,INA219 will run with 32V,2A calibration
  This is because,it should initialize and keep running
  at highest possible sale to keep things safe 
  */
}


void loop() {
  //get,voltage,current and power and dump them all in the display
  
  V=get_voltage();
  I=get_current();
  P=get_power();

  if(update_disp==true)
  {
    update_disp=false;
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
}

void init_display()
{
  oled_handler.begin(SSD1306_SWITCHCAPVCC);
  delay(100);
  oled_handler.clearDisplay();
  oled_handler.setCursor(0,0);
  oled_handler.setTextSize(1);
  oled_handler.setTextColor(WHITE);
  oled_handler.println("initializing...");
  oled_handler.display();
}

/*since at no    load,the output of INA219 tends to be erroneous
 * we will write a function to check the shunt voltage,if its negative
 * simply output 0
*/

float get_voltage()
{
   float bus_V=0.0; //bus voltage
   float shunt_V=0.0; //voltage drop across the shunt,
   float total_V=0.0; //bus+shunt
   float i_mA=pm_handler.getCurrent_mA();
   shunt_V=pm_handler.getShuntVoltage_mV();
   bus_V=pm_handler.getBusVoltage_V();
   total_V=bus_V+(shunt_V/1000.0);
   if(i_mA<1.0)
   {
    if(total_V<=1.03) return 0.00;
   }
   return total_V;
}

/*
 * same goes about current
 */
float get_current()
{
  float i_mA=0.0;
  i_mA=pm_handler.getCurrent_mA();
  if(i_mA<0) return 0.0;
  if(i_mA>=1000.0)
  {
    i_mA=i_mA/1000.0;
    i_unit="A";
    return i_mA;
  }
  i_unit="mA";
  return i_mA;
}

float get_power()
{
  float V=0.0;
  float I=0.0;
  float P=0.0;
  V=get_voltage();
  I=get_current();
  P=V*I;
  if(P>=1000) 
  {
    p_unit="W";
    return P/1000.0;
  }
  p_unit="mW";
  return P;
}

void send_data_serial(float V,float I,float P)
{
  Serial.print(V);
  Serial.print(",");
  Serial.print(I);
  Serial.print(",");
  Serial.print(i_unit);
  Serial.print(",");
  Serial.print(P);
  Serial.print(",");
  Serial.println(p_unit);
  
}


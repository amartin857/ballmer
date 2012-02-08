#include "DrinkShield.h"

// 0.1 is the version written on the DrinkShield board
DrinkShield ds(0,1);

int highscoreLed = 0;  // The highest LED
int lightLevel;        // Current LED level

int highVal = 0; // highest value from sensor
int currentVal;  // current value from sensor
int timesRegistered = 0; // stops high value from hitting serial connection more than once

void setup()
{
  // Take 20 air samples when we first turn on the system
 ds.autocalibrate(20);
 // Turn on the Ready light and turn off the rest
 ds.greenLight(ON);
 ds.redLight(OFF);
 ds.lightBarLevel(0, 0);
 Serial.begin(9600);
}

void loop()
{
        
   // unless we've sent a high water mark reading, send 0
   if(timesRegistered < 1) {
     Serial.print("0\n");
   }
    
  int val = ds.getReading();
  
  if(val) {  // Get & display a reading

    currentVal = val;
    lightLevel = ds.getLightLevel(val);
    
    if(lightLevel > highscoreLed) {
      highscoreLed = lightLevel;
    }
    
    // increment the high val if the current val is higher... 
    if(currentVal > highVal) {
      highVal = currentVal; 
    }
      
    // until the current val drops below high val -
    // this means we've hit the high water mark;
    // or more acurately, the high alcohol mark.
    if( (timesRegistered < 1) && (currentVal < highVal) ) {
      Serial.print( String(highVal) );
      timesRegistered = 1;
    }

      
    ds.lightBarLevel(lightLevel, highscoreLed);
    
  } else if(highscoreLed) {  // Done.  Flash and reset
    
    for(int cnt=0; cnt < 4; cnt++) {
     ds.lightBarLevel(0, highscoreLed);
     delay(100);
     ds.lightBarLevel(0, 0);
     delay(100); 
    }

    highscoreLed = 0;
  }
}

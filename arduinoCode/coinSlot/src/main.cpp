#include <Arduino.h>


int coin = 2;
int i = 0;
int impulsCount = 0;
float total_amount = 0;
float previous_total = 0; 

void incomingImpuls() {
  impulsCount = impulsCount + 1;
  i = 0;
}

void setup() {
  pinMode(coin, INPUT_PULLUP);
  Serial.begin(9600);
  attachInterrupt(0, incomingImpuls, FALLING);
}



void loop() {

  // Serial.println(digitalRead(coin)); 
  i = i + 1;

  if (i >= 30 && impulsCount == 1) {
    total_amount = total_amount + 1;
    impulsCount = 0;
  }
  if (i >= 30 && impulsCount == 5) {
    total_amount = total_amount + 5;
    impulsCount = 0;
  }
  if (i >= 30 && impulsCount == 10) {
    total_amount = total_amount + 10;
    impulsCount = 0;
  }

 
  if (total_amount != previous_total) {
    
    Serial.print("Total: ");
    Serial.println(total_amount);
    
    previous_total = total_amount;
  }
}
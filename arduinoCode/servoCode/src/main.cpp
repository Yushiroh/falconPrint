#include <Arduino.h>
#include <Servo.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 53
#define RST_PIN 8

MFRC522 mfrc522(SS_PIN, RST_PIN);  

const int butA = 5;
const int butB = 6;
const int butC = 7;

int coin = 2;
int i = 0;
int impulsCount = 0;
int total_amount = 0;
int previous_total = 0; 
String amountString = "0";

Servo servA;
Servo servB;

void incomingImpuls() {
  impulsCount = impulsCount + 1;
  i = 0;
}

void setup() {
   Serial.begin(9600);


   servA.attach(3);
   servB.attach(4);

   pinMode(butA, INPUT_PULLUP);
   pinMode(butB, INPUT_PULLUP);
   pinMode(butC, INPUT_PULLUP);

   pinMode(coin, INPUT_PULLUP);
   attachInterrupt(0, incomingImpuls, FALLING);

   SPI.begin();   
   mfrc522.PCD_Init();

}

void loop() {

  // Serial.print(digitalRead(butA));
  // Serial.print(digitalRead(butB));
  // Serial.println(digitalRead(butC));

  if(digitalRead(butA) == 1 and digitalRead(butB) == 1 and digitalRead(butC) == 1){
    servA.write(30);
    servB.write(30);
    Serial.println("Servo30...");
  }else if(digitalRead(butA) == 1 and digitalRead(butB) == 0 and digitalRead(butC) == 1){
   //CoinSlotMode
   //  Serial.println("CoinMode");
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

      if(total_amount < 10){
         amountString = "0" + String(total_amount);
         previous_total = total_amount;
      }else{
         amountString = String(total_amount);
         previous_total = total_amount;
      }
    }else{

      if(amountString.length() == 1){
          Serial.print(amountString);
      }else{
          Serial.print(amountString); 
      }

    }
    servA.write(0);
    servB.write(0);
    
  }else if(digitalRead(butA) == 1 and digitalRead(butB) == 1 and digitalRead(butC) == 0){

   if ( ! mfrc522.PICC_IsNewCardPresent()) 
   {
      return;
   }
   if ( ! mfrc522.PICC_ReadCardSerial()) 
   {
      return;
   }
   String content= "";
   for (byte i = 0; i < mfrc522.uid.size; i++) 
   {
      content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
      content.concat(String(mfrc522.uid.uidByte[i], HEX));
      
   }

   content.toUpperCase();
   Serial.println();
   Serial.println(content);

  }else{
    servA.write(0);
    servB.write(0);
  }

}

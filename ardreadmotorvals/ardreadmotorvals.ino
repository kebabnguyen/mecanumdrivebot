#include <Servo.h>

Servo escs[4]; //0   1    2    3
int escpins[4] =  {3,  9,  10,  11};
// associated as FL, FR,  BR,  BL

int fullRev = 500;
int fullFor = 2500;
int readings[4];
int readtrack = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i = 0; i < 4; i++)
  {
    escs[i].attach(escpins[i], fullRev, fullFor);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0)
  {
    for (int i = 0; i < 4; i ++)
    {
      readings[i] = Serial.parseInt();
      if(readings[i] == 0)
        readings[i] = 1500;
      escs[i].writeMicroseconds(readings[i]);
      Serial.print(readings[i]);
      Serial.print(" ");
    }
    Serial.println();
  } 
}

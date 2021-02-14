#include <Servo.h>

Servo escs[4]; //0   1    2    3
int escpins[4] =  {3,  9,  10,  11};
// associated as FL, FR,  BR,  BL

int fullRev = 500; //limits on pulse width via datasheet
int fullFor = 2500;
int readings[4];


void setup() {
  Serial.begin(9600);
  for(int i = 0; i < 4; i++) //the escs can be controlled from software side as servos w/ pwm
  {
    escs[i].attach(escpins[i], fullRev, fullFor);
  }
}

void loop() {
  if(Serial.available() > 0)
  {
    for (int i = 0; i < 4; i ++)
    {
      readings[i] = Serial.parseInt(); //read int sent from serial
      if(readings[i] == 0) //sometimes parseInt() would time out and return 0, 
        readings[i] = 1500; //causing whichever reading to go full reverse
      escs[i].writeMicroseconds(readings[i]);
      //Serial.print(readings[i]); debug
      //Serial.print(" "); debug
    }
    //Serial.println(); debug
  } 
}

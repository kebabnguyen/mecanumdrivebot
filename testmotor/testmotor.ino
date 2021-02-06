#include <Servo.h>

Servo escFL, escFR, escBR, escBL;
int pwm1 = 3; // pwm pins are 9, 10, 11, and 3
int pwm2 = 9;
int pwm3 = 10;
int pwm4 = 11;

int fullRev = 500;
int fullFor = 2500;
int t = 0;   // declares variable t
int pot;
void setup()  // setup loop
{
  Serial.begin(9600);
  escFL.attach(pwm1, fullRev, fullFor);
  escFR.attach(pwm2, fullRev, fullFor);
  escBR.attach(pwm3, fullRev, fullFor);
  escBL.attach(pwm4, fullRev, fullFor);

}

void testServo(int parVal)
{
  escFL.writeMicroseconds(1500 + parVal);
  escFR.writeMicroseconds(1500 - parVal);
  escBR.writeMicroseconds(1500 - parVal);
  escBL.writeMicroseconds(1500 + parVal);
}

void testManuel(int parVal)
{
  int t1 = parVal;
  int t2 = 2500 - t1;
  digitalWrite(pwm1, HIGH);
  digitalWrite(pwm2, HIGH);
  digitalWrite(pwm3, HIGH);
  digitalWrite(pwm4, HIGH);
  delayMicroseconds(t1);
  digitalWrite(pwm1, LOW);
  digitalWrite(pwm2, LOW);
  digitalWrite(pwm3, LOW);
  digitalWrite(pwm4, LOW);
  delayMicroseconds(t2);

}
void loop()
{
//  pot = analogRead(5);
//  pot = map(pot, 0, 1023, fullRev, fullFor);
//  Serial.print(pot);
//  Serial.println();
  testServo(500);
  
  
}

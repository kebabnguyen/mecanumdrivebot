#include <Servo.h>

Servo esc1, esc2, esc3, esc4;
int pwm1 = 9; // pwm pins are 9, 10, 11, and 6
int pwm2 = 10;
int pwm3 = 11;
int pwm4 = 3;

int fullRev = 500;
int fullFor = 2500;
int t = 0;   // declares variable t
int pot;
void setup()  // setup loop
{
  Serial.begin(9600);
  esc1.attach(pwm1, fullRev, fullFor);
  esc2.attach(pwm2, fullRev, fullFor);
  esc3.attach(pwm3, fullRev, fullFor);
  esc4.attach(pwm4, fullRev, fullFor);

}

void testServo(int parVal)
{
  esc1.writeMicroseconds(parVal);
  esc2.writeMicroseconds(parVal);
  esc3.writeMicroseconds(parVal);
  esc4.writeMicroseconds(parVal);
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
  pot = analogRead(5);
  pot = map(pot, 0, 1023, fullRev, fullFor);
  Serial.print(pot);
  Serial.println();
  testServo(pot);
  
  
}

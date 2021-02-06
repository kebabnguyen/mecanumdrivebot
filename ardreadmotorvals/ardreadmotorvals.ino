
int readings[4];
int readtrack = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0)
  {
    readings[readtrack] = Serial.parseInt();
    if(readtrack > 3)
      readtrack = 0;
    else
      readtrack++;
    for (int i = 0; i < 4; i ++)
    {
      Serial.print("motor ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(readings[i]);
    }
  }
  
}

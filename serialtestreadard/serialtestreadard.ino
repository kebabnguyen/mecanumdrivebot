int incomingByte = 0; // for incoming serial data
int num = 0;

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read() - 48;

    if(incomingByte == -35)
    {
      Serial.print("I received: ");
      Serial.println(num);
      num = 0;
      Serial.println("New number!");
    }
    else
    {
    num = num*10+incomingByte;
    }
    

  }
}

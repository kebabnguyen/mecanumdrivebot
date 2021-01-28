int incomingByte = 0; // for incoming serial data
int num = 0;

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}

void loop() {
  //check if serial buffer is nonempty
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read(); 

    //incomingByte is read as an ascii value, 13 is carriage return, 10 is newline
    switch(incomingByte) 
    {
      case 13:
      Serial.print("received: ");
      Serial.println(num);
      num = 0;
      break;
      case 10:
      break;
      default:
      num = num*10 + (incomingByte - 48);
    }

    

  }
}

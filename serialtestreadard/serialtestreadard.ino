#include <math.h>

int incomingByte = 0; // for incoming serial data
int num = 0; //storing read number


void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  
}

void printParse()
{
  if (Serial.available() > 0)
  {
    // read the incoming byte:
    incomingByte = Serial.read(); 

    //incomingByte is read as an ascii value, 13 is carriage return, 10 is newline
    switch(incomingByte) 
    {
      case 13:
      Serial.print("readin: ");
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

int readIn() //work on this
{
  if (Serial.available() > 0)
  {
    // read the incoming byte:
    incomingByte = Serial.read(); 

    //incomingByte is read as an ascii value, 13 is carriage return, 10 is newline
    switch(incomingByte) 
    {
      case 13:
      Serial.print("readin: ");
      Serial.println(num);
      break;
      case 10:
      int readInt = num;
      num = 0;
      return (readInt);
      break;
      default:
      num = num*10 + (incomingByte - 48);
    }
  }
}

void intRead()
{
  if(Serial.available() > 0)
  {
    Serial.print("returned: ");
    Serial.println(Serial.parseInt(SKIP_ALL));
  }
    
}
void loop() {
  if (Serial.available() > 0)
  {
    // read the incoming byte:
    incomingByte = Serial.read(); 

    //incomingByte is read as an ascii value, 13 is carriage return, 10 is newline
    switch(incomingByte) 
    {
      case 13:
      Serial.print("readin: ");
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

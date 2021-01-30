#include <math.h>

int incomingByte = 0; // for incoming serial data
int num = 0; //storing read number
int test = 0;
int readings[4];
int inc = 0;


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
    int readInt;
    //incomingByte is read as an ascii value, 13 is carriage return, 10 is newline
    switch(incomingByte) 
    {
      case 13:
      readInt = num;
      //Serial.print("returning: ");
      //Serial.println(readInt);
      break;
      case 10:
      num = 0;  
      break;
      default:
      num = num*10 + (incomingByte - 48);
    }
    return (readInt);
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
void loop() { //still wip, focusing on doing math on pi side before sending over
  if(Serial.available() > 0)
  {
   readings[inc] = readIn();
   Serial.println(readings[inc]);
   inc++;
   if(inc == 3)
   {
      inc = 0;
   }
  }
  
  
}

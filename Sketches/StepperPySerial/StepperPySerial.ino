#include <SPI.h>

#define stepPin 3
#define dirPin 4
#define DebugLED 13
#define LeftSwitch A0;
#define RightSwitch A1;

//Received Byte-Int Array
int received[2]; int steps = 0;
bool leftSwitch, rightSwitch = false;
bool newData = true; int cw = 1;

//Constant Variables
const int maxSpeed = 375; //375 is maximum possible speed
const int minSpeed = 2000; //1000-5000 is pretty slow

void setup() {
  // Sets Outputs / Serial BaudRate (Recommended <=115200 baud)
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(DebugLED, OUTPUT);
	pinMode(LeftSwitch, INPUT);
	pinMode(RightSwitch, INPUT);
	digitalWrite(DebugLED, LOW);
  Serial.begin(115200); 
}

void readData() {
  if (Serial.available() > 1) {
    digitalWrite(DebugLED, HIGH);
    int byteLength = Serial.available();
    for(int i=0; i<byteLength; i++) {
      received[i] = Serial.read();
      newData = true;
    }
    cw = (received[0] & 128) ? 1 : -1;

    return (received[0] & 170), received[1];
  }
  else {
    digitalWrite(DebugLED, LOW);
    newData = false;
  }
  Serial.flush();
}

void stepAmountSpeed(int steps, int speed) {
  //Takes Unlimited Step Count Int and Speed 1-100
  
  //Change Polarity Of Motor
  if (cw==1) {digitalWrite(dirPin, HIGH);}
  else {digitalWrite(dirPin, LOW);}

  //Map the speed and cache
  int modulatedSpeed = int(map(speed, 0, 100, minSpeed, maxSpeed));
  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(modulatedSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(modulatedSpeed);
    stepCount += cw;
  }
}

void loop() {
  //Grab The Step Amount as Well as Step Speed From Serial Bytes
  int stepAmount, int rotationSpeed = readData();
  Serial.write(stepAmount, rotationSpeed);
}

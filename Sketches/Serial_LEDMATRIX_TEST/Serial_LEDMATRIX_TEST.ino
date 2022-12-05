#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define Interrupt_LED 2

int throttle[4] = {1, 3, 4, 5};
int steering[4] = {2, 6, 7, 8};
RF24 radio(9, 10); // CE, CSN         
const uint64_t pipe = 0xE6E6E6E6E6E6; // Needs to be the same for communicating between 2 NRF24L01 
int SentMessage[1] = {000};

char received = 'A';
boolean newData = false;

void singleOutput(int pin, int pins[]){
  for (int i=0; i<4; i++){ 
    if (pin == pins[i]){
      digitalWrite(pins[i], HIGH);   
    }
    else {
      digitalWrite(pins[i], LOW);
    }
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  for(int i=0; i<4; i++){
    pinMode(throttle[i], OUTPUT);
    pinMode(steering[i], OUTPUT);
  }
  singleOutput(4, throttle);
  singleOutput(7, steering);
  Serial.flush();
  radio.begin();
  radio.openWritingPipe(pipe); //Setting the address where we will send the data
  //radio.setPALevel(RF24_PA_MIN);  //You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
  //radio.setRetries(1, 1);//time,re tries
  //radio.stopListening();          //This sets the module as transmitter
  //Bababooey, Spaghetti. Did I Copy The Code? I Forghetti
  pinMode(Interrupt_LED, 2);
  digitalWrite(Interrupt_LED, HIGH);
}

void receiveData() {
  if (Serial.available() > 0) {
    received = Serial.read();
    digitalWrite(Interrupt_LED, HIGH);
    newData = true;
  }
  else{
    digitalWrite(Interrupt_LED, LOW);
  }
}

void processData() {
  switch (received) {
    case 'A':
      singleOutput(4, throttle);
      sendData();
      break;
    case 'B':
      singleOutput(3, throttle);
      sendData();
      break;
    case 'C':
      singleOutput(5, throttle);
      sendData();
      break;
    case 'D':
      singleOutput(7, steering);
      sendData();
      break;
    case 'E':
      singleOutput(6, steering);
      sendData();
      break;
    case 'F':
      singleOutput(8, steering);
      sendData();
      break;
    default:
      newData = false;
      break;
  }
}

void sendData() {
  // Serial.print(received)
  SentMessage[0] = 111;
  Serial.println("Starting Message");
  radio.write(SentMessage, 1);
  Serial.println("Sent Message");
  newData = false;
}

void loop() {
  //Send And Receive Data
  receiveData();
  processData();
}

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define LED 13
#define PWMPin 5

int received = 0;
boolean newData = false;
int kart_speed = 0;

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

  singleOutput(4, throttle);
  singleOutput(7, steering);
  Serial.flush();
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

int processData() {
  if (newData) {
    kart_speed = min(received, 100);
  }
  else {
    kart_speed = 0;
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
  analogWrite()
}

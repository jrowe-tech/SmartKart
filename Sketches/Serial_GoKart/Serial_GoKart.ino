#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define LED 13
#define PWMPin 5

int received = 0;
bool newData = false;

void setup() {
  Serial.begin(115200);
  Serial.flush();

  pinMode(PWMPin, OUTPUT);
  pinMode(LED, OUTPUT);

  analogWrite(PWMPin, LOW);
  digitalWrite(LED, LOW);
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
  if (newData) {
    kartSpeed = received;
    newData = False;

    digitalWrite(LED, HIGH);
  }
  else {
    kartSpeed = 0;

    digitalWrite(LED, LOW);
  }

  kartSpeed = max(min(kartSpeed, 100), 0);
  float convertedSpeed = (kartSpeed * 255) / 100;

  return round(convertedSpeed);
}

void loop() {
  //Send And Receive Data
  receiveData();
  analogWrite(PWMPin, processData());
}

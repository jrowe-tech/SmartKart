#include <Firmata.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN    
const byte address[6] = "00001";  

byte previousPIN[TOTAL_PORTS];  // PIN means PORT for input
byte previousPORT[TOTAL_PORTS];

int package = 0;
/*
 * Bit System Here -> **** -> 0000 / 1111
 * 1*** -> Throttle On
 * *1** -> Throttle Positive ***IGNORE IF BIT 1 IS 0***
 * **1* -> Steering On
 * ***1 -> Steering Positive ***IGNORE IF BIT 3 IS 0***
*/

void setStringCallback(String data){
  Serial.println(data)
  package = data.toInt();
}

void outputPort(byte portNumber, byte portValue)
{
  // only send the data when it changes, otherwise you get too many messages!
  if (previousPIN[portNumber] != portValue) {
    Firmata.sendDigitalPort(portNumber, portValue);
    previousPIN[portNumber] = portValue;
  }
  radio.begin();  
  radio.begin();                  //Starting the Wireless communication
  radio.openWritingPipe(address); //Setting the address where we will send the data
  radio.setPALevel(RF24_PA_MIN);  //You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.stopListening();          //This sets the module as transmitter
}

void setPinModeCallback(byte pin, int mode) {
  if (IS_PIN_DIGITAL(pin)) {
    pinMode(PIN_TO_DIGITAL(pin), mode);
  }
}

void digitalWriteCallback(byte port, int value)
{
  byte i;
  byte currentPinValue, previousPinValue;

  if (port < TOTAL_PORTS && value != previousPORT[port]) {
    for (i = 0; i < 8; i++) {
      currentPinValue = (byte) value & (1 << i);
      previousPinValue = previousPORT[port] & (1 << i);
      if (currentPinValue != previousPinValue) {
        digitalWrite(i + (port * 8), currentPinValue);
      }
    }
    previousPORT[port] = value;
  }
}

void setup()
{
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION, FIRMATA_FIRMWARE_MINOR_VERSION);
  Firmata.attach(DIGITAL_MESSAGE, digitalWriteCallback);
  Firmata.attach(SET_PIN_MODE, setPinModeCallback);
  Firmata.attach(STRING_DATA, setStringCallback);
  Firmata.begin(57600);
}

void loop()
{
  byte i;

  for (i = 0; i < TOTAL_PORTS; i++) {
    outputPort(i, readPort(i, 0xff));
  }

  while (Firmata.available()) {
    Firmata.processInput();
  }

  radio.write(&package, sizeof(package));  
  Serial.println(&package)
}

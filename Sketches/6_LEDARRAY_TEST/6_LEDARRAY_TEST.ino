int pins[7] = {2, 3, 4, 5, 6, 7, 8};
int pinCount = 7;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  for(int pin = 0; pin < pinCount; pin++){
    pinMode(pins[pin], OUTPUT);
    digitalWrite(pins[pin], LOW);
  }
}

int iter = 0;
void loop() {
  // put your main code here, to run repeatedly:
  if(iter == pinCount){
    iter = 0;
    digitalWrite(pins[6], LOW);
  }
  digitalWrite(pins[iter], HIGH);
  digitalWrite(pins[iter-1], LOW);
  delay(100);
  iter++;
}  

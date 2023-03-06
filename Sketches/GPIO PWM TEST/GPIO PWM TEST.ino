#define pwmOne 5
#define pwmTwo 6

int _delay = 2000;

void setup() {
  // put your setup code here, to run once:
  pinMode(pwmOne, OUTPUT);
  pinMode(pwmTwo, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(pwmOne, HIGH);
  digitalWrite(pwmTwo, LOW);
  delay(_delay);
  digitalWrite(pwmOne, LOW);
  digitalWrite(pwmTwo, HIGH);
  delay(_delay);
}

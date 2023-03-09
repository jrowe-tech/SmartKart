#define pwmOne 5
#define pwmTwo 6
#define pwmThree 3

int _delay = 200;
int starting_speed = 60;
int inc = starting_speed;
int max_speed = 255;

void setup() {
  // put your setup code here, to run once:
  pinMode(pwmOne, OUTPUT);
  pinMode(pwmTwo, OUTPUT);
  digitalWrite(pwmOne, LOW);
  digitalWrite(pwmTwo, LOW);
  analogWrite(pwmThree, starting_speed);
}

void speed_up_alt() {
  digitalWrite(pwmTwo, LOW);

  inc = starting_speed;
  while (inc <= max_speed) {
    analogWrite(pwmOne, inc);
    delay(_delay);
    inc += 5;
  }

  digitalWrite(pwmOne, LOW);
  
  inc = starting_speed;
  while (inc <= max_speed) {
    analogWrite(pwmTwo, inc);
    delay(_delay);
    inc += 5;
  }  
}

void back_forth() {
  digitalWrite(pwmTwo, LOW);
  analogWrite(pwmOne, max_speed);
  delay(500);
  digitalWrite(pwmOne, LOW);
  analogWrite(pwmTwo, max_speed);
  delay(500);
}

void loop() {
  //speed_up_alt();
  back_forth();
}

#define analogPin A0
#define PWMPin 3

// 1 MHz is optimal frequency w/ 1kOhm + 0.1uF Capacitor
int frequency = 1000000;

// Output Voltage -> Measure Mean Average Deviation
float voltageOut = 0.00;

// Output PWM Step
float voltageStep = 0.1000;

// Amount Of Values To Measure(Up To 100000)
int measureCount = 5000;

// Measurement Configuration Constant -> More Accurate Measurements
float analogReadConstant = 1;

//Create 1023 10-Bit Conversion (Arduino Only Has 0-5V Analog Input)
double conversionFactor = double(5) / 1023;

// Create 256 8-Bit Conversion (Arduino Only Has 0-255 Analog Output PWM)
double PWMconstant = double(255) / 5;

// Create Average Storage Variables
float averageVoltage;
float averageDeviation;

// Create Float Derivative Out
float dOut = 0;

// Create Loop Counter
int loopCounter = 1;

void setup() {
  // put your setup code here, to run once:
  pinMode(analogPin, INPUT);
  pinMode(PWMPin, OUTPUT);
  averageVoltage = 0.000;
  averageDeviation = 0.000;
  Serial.begin(9600);
  delay(3000);
}

bool StepPWM(){
  if (voltageOut < 4.999){
    voltageOut += voltageStep;
    //digitalWrite(PWMPin, HIGH);
    analogWrite(PWMPin, int(voltageOut * PWMconstant));
    return true;
  }
  else {
    Serial.println("DEACTIVATED");
    return false;
  }
}

double readData() {
  double data = analogRead(analogPin) * conversionFactor * 2 / analogReadConstant;
  return data;
}


void loop() {
  //Update PWM Values
  bool active = StepPWM();
  if (active) {
    //Set Running Averages
    averageVoltage = 0; averageDeviation = 0;
    for (int i = 1; i < measureCount; i++) {
      float reading = readData();
      //Serial.println("Voltage Detected: " + String(reading));
      averageVoltage = ((averageVoltage * (i - 1)) + reading) / i;
      averageDeviation = ((averageDeviation * (i - 1)) + abs(voltageOut - reading)/voltageOut) / i;
    }
    delay(50);
    Serial.print("Voltage Out: " + String(voltageOut));
    Serial.print(" | Average Voltage Value: " + String(averageVoltage));
    Serial.print(" | Average Percent Error: " + String(averageDeviation * 100) + "%");
    Serial.println(" | dVin / dVout: " + String(dOut));
    dOut = averageVoltage / voltageOut; //((dOut * (loopCounter - 1)) + (averageVoltage / voltageOut)) / loopCounter;
    
    loopCounter++;
  }
}

#include <Servo.h>

int servoPin = 9;
Servo servo;
int incoming[5];

void setup() {
  // put your setup code here, to run once:
  servo.attach(servoPin);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() >= 5) {
    for (int i = 0; i < 5; i++) {
      incoming[i] = Serial.read();
    }
    for (int i = 0; i < 5; i++) {
      servo.write(30);
      delay(1000 * incoming[i]);
    }
  }
}

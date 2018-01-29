const byte ledPin = 13;
const byte interruptPin = 2;
volatile byte state = HIGH;
unsigned long lastTime = millis();
unsigned long timeDiff = millis();

unsigned long rotations = 0;
float wheel_c = 1.7; // Circumference of wheel
float last_distance = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), blink, CHANGE);
  Serial.begin(9600);

}

void loop() {
  float new_distance = rotations * wheel_c;
  float diff = new_distance - last_distance;
  digitalWrite(ledPin, state);
  Serial.print(diff * 10); // m/s
  Serial.print(",");
  Serial.println(new_distance);
  delay(100);
  last_distance = new_distance;
}

void blink() {
  state = !state;
  rotations ++;
  unsigned long CurrentTime = millis();
  timeDiff = CurrentTime - lastTime;
  lastTime = CurrentTime;
}

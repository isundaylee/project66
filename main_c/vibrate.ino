int vPin = 3;
int vPhase;
int vPWM;

void vibrate(int vT) {
  vPhase = millis() % vT;
  if (vPhase < 0.2 * vT) {
    vPWM = 128;
  }
  else if (vPhase < 0.4 * vT) {
    vPWM = 16;
  }
  else if (vPhase < 0.6 * vT) {
    vPWM = 128;
  }
  else {
    vPWM = 16;
  }
  analogWrite(vPin, vPWM);
}


// the setup function runs once when you press reset or power the board
void setup() {
  pinMode(vPin, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  vibrate(250); //250 to 750 works well
}
#include <ClickButton.h>
#include <Encoder.h>

int vPin = 9;
int vPhase;
int vPWM;

void vibrate(int vT) {
  if (vT == 0) {
    digitalWrite(vPin, LOW);
    return;
  }
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

Encoder myEnc(2,3);
const int encButtonPin = 7;
const int clickButtonPin = 6;
const int rLED = 11;
const int gLED = 10;
ClickButton encButton(encButtonPin, LOW, CLICKBTN_PULLUP);
ClickButton clickButton(clickButtonPin, LOW, CLICKBTN_PULLUP);


void setup() {
  Serial.begin(115200);
  pinMode(vPin, OUTPUT);
  pinMode(rLED, OUTPUT);
  pinMode(gLED, OUTPUT);
  encButton.multiclickTime = 1;
  clickButton.multiclickTime = 125;
  clickButton.longClickTime = 500;
  Serial.println("Basic Encoder Test:");
  digitalWrite(rLED, HIGH);
  digitalWrite(gLED, LOW);
}

long curPosition  = -999;
int mode = 0;
long positions[3] = {0,0,0};
long offset = 0;
long lastprint = 0;
long curTime;
int numClicks = 0;
long clickTime = 0;

void loop() {
  curTime = millis();
  clickButton.Update();
  if (clickButton.clicks != 0) {
    numClicks = clickButton.clicks;
    clickTime = curTime;
  }
  
  encButton.Update();
  if(encButton.clicks != 0) {
    mode = (int) (mode + 1 ) % 3;
    offset = -curPosition + positions[mode];
    if (mode == 0) {
      digitalWrite(rLED, HIGH);
      digitalWrite(gLED, LOW);
    }
    if (mode == 1) {
      digitalWrite(gLED, HIGH);
      digitalWrite(rLED, LOW);
    }
    if (mode == 2) {
      digitalWrite(gLED, HIGH);
      digitalWrite(rLED, HIGH);
    }
  }
  
  long newPosition = myEnc.read();
  if (newPosition != curPosition) {
    curPosition = newPosition;
    positions[mode] = curPosition + offset;
  }
  if (curTime > lastprint + 50) {
    lastprint = curTime;
    Serial.print(mode);
    Serial.print(" ");
    Serial.print(positions[mode]);
    Serial.print(" ");
    Serial.print(clickTime);
    Serial.print(" ");
    Serial.print(numClicks);
    Serial.print("\n");
  }
}
/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://arduino.cc

  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
 */
 
#define POLYGON 1
#define CURVE 2

#define SWITCH_THRESHOLD 50
#define SWITCH_HOLD_THRESHOLD 500
#define SWITCH_DOUBLECLICK_THRESHOLD 300
#define INFINITY 0x7fffffff; 

const int dummy = 0; 

int delayed_click = 0; 

int maximumRange = 2000; // Maximum range needed
int minimumRange = 0; // Minimum range needed
long duration, distance; // Duration used to calculate distance
int click_type = 0;
int clicking = 0;
int curving = 0;
int calA = 122;
int calB = 123;
int calC = 130;

int curve_rep = 0;

int mode = POLYGON; 

#define clickpin 2
#define curvepin 3
#define resetA 4
#define resetB 5
#define resetC 6
#define Atrig 7
#define Aecho 8
#define Btrig 11
#define Becho 12
#define Ctrig 0
#define Cecho 1
#define vibrate 9


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  Serial.begin(9600);
  pinMode(clickpin, INPUT);
  pinMode(curvepin, INPUT);
  pinMode(resetA, INPUT);
  pinMode(resetB, INPUT);
  pinMode(resetC, INPUT);
  pinMode(Atrig, OUTPUT);
  pinMode(Aecho,INPUT);
  pinMode(Btrig, OUTPUT);
  pinMode(Becho,INPUT);
  pinMode(Ctrig, OUTPUT);
  pinMode(Cecho,INPUT);
//  pinMode(Cpin, INPUT); 
  pinMode(vibrate, OUTPUT);
  attachInterrupt(clickpin, clicks, RISING);
  attachInterrupt(curvepin, int_curve, CHANGE);
}

void int_curve() {
  static int last_high = INFINITY; 
  
  if (digitalRead(curvepin) == HIGH) {
    last_high = millis(); 
  } else {
    int duration = millis() - last_high; 
    
    if (duration > SWITCH_THRESHOLD) {
      if (mode == POLYGON) {
        mode = CURVE;
        Serial.println("mode curve");
      } else {
        mode = POLYGON;
        Serial.println("mode polygon"); 
      }
    }
    
    last_high = INFINITY;  
  }
}

void int_click() {
  static int last_high = INFINITY; 
  static int last_click = 0; 
  
  if (digitalRead(clickpin) == HIGH) {
    last_high = millis(); 
  } else {
    int duration = millis() - last_high; 
    
    Serial.println(last_click); 
    
    if (duration > SWITCH_HOLD_THRESHOLD) {
      Serial.println("hold"); 
    } else if (duration > SWITCH_THRESHOLD) {
      if (millis() - last_click < SWITCH_DOUBLECLICK_THRESHOLD) {
        Serial.println("doubleclick"); 
        last_click = 0; 
      }
      
      last_click = millis(); 
      
      delay(300); 
      
      if (millis() - last_click > 200) {
        Serial.println("click"); 
      }
    }
    
    last_high = INFINITY;  
  }
}

void int_curve_high() {
  curve_rep ++; 
  Serial.println("high triggered"); 
}

void int_curve_falling() {
  Serial.println("falling triggered"); 
  if (curve_rep > SWITCH_THRESHOLD) {
  }
  
  curve_rep = 0; 
}

// the code that will jump to if the user clicks
void clicks() {
  clicking++;
  click_type++;
}
// the code that will jump to if the user press curve
void curve() {
  Serial.println("######################");
  Serial.println("######################");
  Serial.println("######################");
  Serial.println("######################");
  Serial.println("######################");
  Serial.println("######################");
  Serial.println("######################");
  Serial.println("######################");
  curving++;
}
// calibration mode
void setA() {
  calA = getDistance(Atrig,Aecho);
}
void setB() {
  calB = getDistance(Btrig,Becho);
}
void setC() {
  calC = getDistance(Ctrig,Cecho);
}


// get the distance from the ultrasonar
int getDistance(int trigPin, int echoPin) {
/* The following trigPin/echoPin cycle is used to determine the
 distance of the nearest object by bouncing soundwaves off of it. */
 digitalWrite(trigPin, LOW);
 delayMicroseconds(2);
 
 digitalWrite(trigPin, HIGH);
 delayMicroseconds(10);
 
 digitalWrite(trigPin, LOW);
 duration = pulseIn(echoPin, HIGH, 10000);
 
 //Calculate the distance (in mm) based on the speed of sound.
 distance = duration/5.82;
   return (int) distance;
 
 if (distance >= maximumRange || distance <= minimumRange){
 /* Send a negative number to computer and Turn LED ON
 to indicate "out of range" */
   return -1;
 }
 else {
 /* Send the distance to the computer using Serial protocol, and
 turn LED OFF to indicate successful reading. */
   return (int) distance;
 }
}
//done with the getdistance 


int getDistance2(int pin) {
  return analogRead(pin); 
}

// the code that tell the python code 
void switchmode() {
  if (clicking == 0) {
    Serial.println("curve");
  }
  else {
    if (click_type == 1) {
      Serial.println("click");
    }
    else {
      if (click_type == 10) {
        Serial.println("hold");
      }
      else {
        Serial.println("doubleclick");
      }
    }
  }
}

//sendpoints print out the points that we get
void sendpoints(){
  Serial.print("point ");
  Serial.print(getDistance(Atrig,Aecho)+calA);
  Serial.print(" ");
  Serial.print(getDistance(Btrig,Becho)+calB);
  Serial.print(" ");
  Serial.print(getDistance(Ctrig,Cecho)+calC); 
//  Serial.print(getDistance2(Cpin));
  Serial.println();
}

void check_for_clicks() {
  if (clicking != 0) {
    delay(300);
    
    if (digitalRead(clickpin) != 0) {
      while (digitalRead(clickpin) == 1) {
        delay(100);
      }
      click_type = 10;
    }
    
    switchmode();
    clicking = 0;
    click_type = 0;
  }
}

void check_for_nearby() {
  while (Serial.available() > 0) {
    byte incomingByte = Serial.read(); 
    
    if (incomingByte == 'n') {
      digitalWrite(vibrate, HIGH); 
    } else {
      digitalWrite(vibrate, LOW); 
    }
  }
}

// the loop function runs over and over again forever
void loop() {
  // the code that check the click type
  check_for_clicks(); 
  
  sendpoints();
  
//  check_for_nearby(); 
  
  delay(100);
}


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

#include <SPI.h>
#include <WiFi.h>
#include <signal.h>

#define POLYGON 1
#define CURVE 2
#define SCULPT 3
#define EXTRUDE 4

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
#define Atrig 0
#define Aecho 1
#define Btrig 4
#define Becho 5
#define Ctrig 7
#define Cecho 8
#define vibrate 9

// WiFi

WiFiServer server(23); 

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  Serial.begin(9600);
  pinMode(clickpin, INPUT);
  pinMode(curvepin, INPUT);
  pinMode(Atrig, OUTPUT);
  pinMode(Aecho,INPUT);
  pinMode(Btrig, OUTPUT);
  pinMode(Becho,INPUT);
  pinMode(Ctrig, OUTPUT);
  pinMode(Cecho,INPUT);
  pinMode(vibrate, OUTPUT);

  signal(SIGPIPE, SIG_IGN);  

  attachInterrupt(clickpin, clicks, RISING);
  attachInterrupt(curvepin, int_curve, CHANGE);

  server.begin(); 
}

void comm_println(char *msg) {
  Serial.println(msg); 
  server.println(msg); 
}

void comm_print(char *msg) {
  Serial.print(msg);
  server.print(msg); 
}


void comm_print(int v) {
  Serial.print(v);
  server.print(v); 
}

void int_curve() {
  static int last_high = INFINITY; 

  if (digitalRead(curvepin) == HIGH) {
    last_high = millis(); 
  } 
  else {
    int duration = millis() - last_high; 

    if (duration > SWITCH_THRESHOLD) {
      if (mode == POLYGON) {
        mode = EXTRUDE;
        comm_println("mode extrude");
      } 
      else if (mode == EXTRUDE) {
        mode = SCULPT;
        comm_println("mode sculpt"); 
      } 
      else if (mode == SCULPT) {
        mode = CURVE; 
        comm_println("mode curve"); 
      } else if (mode == CURVE) {
        mode = POLYGON; 
        comm_println("mode polygon"); 
      }
    }

    last_high = INFINITY;  
  }
}


// the code that will jump to if the user clicks
void clicks() {
  clicking++;
  click_type++;
}

// get the distance from the ultrasonar
int getDistance(int trigPin, int echoPin) {
  // The following trigPin/echoPin cycle is used to determine the
  // distance of the nearest object by bouncing soundwaves off of it. */
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH, 10000);

  //Calculate the distance (in mm) based on the speed of sound.
  distance = duration/5.82;
  return (int) distance;
}

//sendpoints print out the points that we get
void sendpoints(){
  comm_print("point ");
  comm_print(getDistance(Atrig,Aecho)+calA);
  comm_print(" ");
  comm_print(getDistance(Btrig,Becho)+calB);
  comm_print(" ");
  comm_print(getDistance(Ctrig,Cecho)+calC); 
  comm_println("");
}

void check_for_clicks() {
  if (clicking != 0) {
    comm_println("debug click delaying"); 
    delay(300);

    if (digitalRead(clickpin) != 0) {
      while (digitalRead(clickpin) == 1) {
        delay(100);
      }
      click_type = 10;
    }

    if (click_type == 1) {
      comm_println("click");
    } 
    else if (click_type == 10) {
      comm_println("hold");
    } 
    else {
      comm_println("doubleclick");
    }

    clicking = 0;
    click_type = 0;
  }
}

void check_for_nearby() {
  while (Serial.available() > 0) {
    byte incomingByte = Serial.read(); 

    if (incomingByte == 'n') {
      digitalWrite(vibrate, HIGH); 
    } 
    else {
      digitalWrite(vibrate, LOW); 
    }
  }
}

// the loop function runs over and over again forever
void loop() {
  server.available(); 

  check_for_clicks(); 
  // check_for_nearby(); 

  sendpoints();

  delay(100);
}



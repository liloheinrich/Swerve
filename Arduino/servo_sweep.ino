#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int min_pos = 1;
int max_pos = 180; 
int pos = min_pos;    // variable to store the servo position
int prev_pos = pos;
int min_delay_per_degree = 6;

void setup() {
  myservo.attach(10);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  pos = 90;
  myservo.write(pos);              // tell servo to go to position in variable 'pos'
  delay(min_delay_per_degree*abs(pos-prev_pos));                       
  prev_pos = pos;

//  for (pos = min_pos; pos <= max_pos; pos += 1) { // goes from 0 degrees to 180 degrees in steps of 1 degree
//    myservo.write(pos); // tell servo to go to position in variable 'pos'
//    delay(min_delay_per_degree);  // wait for the servo to reach the position
//  }
//  for (pos = max_pos; pos >= min_pos; pos -= 1) { // goes from 180 degrees to 0 degrees
//    myservo.write(pos); // tell servo to go to position in variable 'pos'
//    delay(min_delay_per_degree);  // wait for the servo to reach the position
//  }
}

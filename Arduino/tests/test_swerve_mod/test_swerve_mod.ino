// Example 5 - Receive with start- and end-markers combined with parsing

#include <Servo.h>

Servo servo1;  // create servo object to control a servo

const byte numChars = 64;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
float motor1_speed = 0.0;
int motorspeed_scalar = 32;
//int motorspeed_scalar = 256;
float motor1_input = 0.0;
int servo1_angle = 0;
int servo1_input = 0;

boolean newData = false;

//============

int SENSOR_PIN = 0; // analog 0 pin of the (fake) potentiometer
int RPWM_Output = 3; // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int LPWM_Output = 5; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)

//============

void setup() {
    Serial.begin(9600);
    servo1.attach(9);
    pinMode(RPWM_Output, OUTPUT);
    pinMode(LPWM_Output, OUTPUT);
//    Serial.println("This demo expects 5 pieces of data - float motor4_speed, and 4 integer servo angles");
//    Serial.println("Enter data in this style <0.676, 12, 24, 171, 90>  ");
//    Serial.println();
}

//============

void loop() {
//  Serial.println(SENSOR_PIN);
    if (Serial.available() > 0){
//  Serial.print("ser available");
      recvWithStartEndMarkers();
//  Serial.print("stop rcv");
      if (newData == true) {
          strcpy(tempChars, receivedChars);
              // this temporary copy is necessary to protect the original data
              //   because strtok() used in parseData() replaces the commas with \0
          parseData();
          showParsedData();
          newData = false;
      }

      servo1_angle = servo1_input;
      servo1.write(servo1_angle);
      motor1_speed = motor1_input * motorspeed_scalar;
      drive_motor(motor1_speed);
    }
    
//  Serial.print("set servo and motor");

//    Serial.flush();
}


// accepts integer in range -256 to 256 ???
// may not want to exceed 32 or 64 cause fast
void drive_motor(float motor_speed) {
  if (motor1_speed < 0) { // reverse rotation
    int reversePWM = abs(motor1_speed);
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, reversePWM);
  } else { // forward rotation
    int forwardPWM = abs(motor1_speed);
    analogWrite(LPWM_Output, forwardPWM);
    analogWrite(RPWM_Output, 0);
  }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '[';
    char endMarker = ']';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
//        Serial.print(rc);

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            } else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        } else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars, ",");
    motor1_input = atof(strtokIndx);     // convert this part to a float

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo1_input = atoi(strtokIndx);     // convert this part to an integer
}

//============

void showParsedData() {
    Serial.print(motor1_input);
    Serial.print(", ");
    Serial.print(servo1_input);
    Serial.println();
}

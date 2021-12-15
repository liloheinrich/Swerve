const byte numChars = 64;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

#include <Servo.h>
#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN1 9
#define PIN2 10
#define NUMPIXELS 90

Adafruit_NeoPixel pixels(NUMPIXELS, PIN1, NEO_RGB + NEO_KHZ800);
Adafruit_NeoPixel pixels2(NUMPIXELS, PIN2, NEO_RGB + NEO_KHZ800);
#define DELAYVAL 500

Servo servo1;
Servo servo2;

// variables to hold the parsed data
float motor1_speed = 0.0;
float motor2_speed = 0.0;
float motor1_input = 0.0;
float motor2_input = 0.0;

int servo1_angle = 0;
int servo2_angle = 0;
int servo1_input = 0;
int servo2_input = 0;


int motorspeed_scalar = 64; // scale speed down, 256 max.

//============

int motor1_RPWM = 3; // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int motor1_LPWM = 11; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)
int motor2_RPWM = 5; 
int motor2_LPWM = 6;
int servo1_PWM = A1;
int servo2_PWM = A0;
//============

boolean newData = false;

//============

void setup() {
  Serial.begin(9600);
  servo1.attach(servo1_PWM);
  servo2.attach(servo2_PWM);
  pinMode(motor1_RPWM, OUTPUT);
  pinMode(motor1_LPWM, OUTPUT);
  pinMode(motor2_RPWM, OUTPUT);
  pinMode(motor2_LPWM, OUTPUT);
  set_speed_to_zero();

  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif

  pixels.begin();
  pixels2.begin();

  for(int i=0; i<NUMPIXELS; i++){
    pixels.setPixelColor(i, pixels.Color(0, 255, 255));
//    pixels.setPixelColor(i, pixels.Color(255, 0, 100));
    pixels.show();
    pixels2.setPixelColor(i, pixels.Color(255, 0, 100));
//    pixels2.setPixelColor(i, pixels.Color(0, 255, 255));
    pixels2.show();
  }

}

//============

void loop() {
    if (Serial.available() > 0){
      recvWithStartEndMarkers();
      if (newData == true) {
          strcpy(tempChars, receivedChars);
              // this temporary copy is necessary to protect the original data
              //   because strtok() used in parseData() replaces the commas with \0
          parseData();
//          showParsedData();
          executeParsedData();
          newData = false;
      }
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

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
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
    motor2_input = atof(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo1_input = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo2_input = atoi(strtokIndx);     // convert this part to an integer
}

//============

void showParsedData() {
    Serial.print(motor1_input);
    Serial.print(", ");
    Serial.print(motor2_input);
    Serial.print(", ");
    Serial.print(servo1_input);
    Serial.print(", ");
    Serial.println(servo2_input);
}

void executeParsedData() {
  servo1_angle = servo1_input;
  servo1.write(servo1_angle);
  motor1_speed = motor1_input * motorspeed_scalar;
  drive_motor(motor1_speed, motor1_RPWM, motor1_LPWM);
  
  servo2_angle = servo2_input;
  servo2.write(servo2_angle);
  motor2_speed = motor2_input * motorspeed_scalar;
  drive_motor(motor2_speed, motor2_RPWM, motor2_LPWM);
}

void drive_motor(float motor_speed, int RPWM_Output, int LPWM_Output) {
  int PWM_speed = abs(motor_speed);
  if (motor_speed < 0) { // reverse rotation
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, PWM_speed);
  } else { // forward rotation
    analogWrite(LPWM_Output, PWM_speed);
    analogWrite(RPWM_Output, 0);
  }
}

void set_speed_to_zero(){
  drive_motor(0, motor1_RPWM, motor1_LPWM);
  drive_motor(0, motor2_RPWM, motor2_LPWM);
}

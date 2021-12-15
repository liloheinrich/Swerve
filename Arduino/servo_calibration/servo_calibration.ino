#include <Servo.h>

Servo servo1;
Servo servo2;

int servo1_angle = 0;
int servo2_angle = 0;

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
}

//============

void loop() {
  servo_angle1 = 0;
  servo_angle2 = 0;
  execute();
  delay(2000);
  
  servo_angle1 = 90;
  servo_angle2 = 90;
  execute();
  delay(2000);
  
  servo_angle1 = 180;
  servo_angle2 = 180;
  execute();
  delay(2000);
}

void execute(){
  servo1.write(servo1_angle);
  servo2.write(servo2_angle);
  
  motor1_speed = 32;
  drive_motor(motor1_speed, motor1_RPWM, motor1_LPWM);
  motor2_speed = 32;
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

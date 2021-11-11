/************************************************
Editor   : MYBOTIC www.mybotic.com.my
Date     : 29 Aug 2014
Project  : 2 Channels Motor Driver Module
*************************************************/

//define motor 1 related pins
#define IN1 9
#define IN2 8
#define ENA 10

//define motor 2 related pins
#define IN3 7
#define IN4 6
#define ENB 5

// this was calibrated with the wheel unattached and therefore not touching the ground
const int min_pwm_speed = 100;
// this is from the analogWrite() doc - the range is 0 to 255
const int max_pwm_speed = 255;

void setup(){ 
  Serial.begin(9600);
  
  //set output for motor 1 related pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  
  //set output for motor 2 related pins
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  
  //set motor 1 run in clockwise
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  
  //set motor 2 run in anticlockwise
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void loop(){

////  0- no beep, 1- beep quiet, 10- beep loud, 100- beep medium, 200- beep quiet, 250- beep quiet, 255- no beep
//// gets slightly louder as i decrease the microsecond timeout
//// I hypothesize current is too low. battery direct works, so it must be the converter or controller. I think its the converter?

//  analogWrite(ENA, 200); //set PWM to Motor 1
//  analogWrite(ENB, 190); //set PWM to Motor 2
//  delay(100); // 100 milliseconds



  fwd_back();

}

void set_motor_dir(int pin1, int pin2, boolean dir) {
  if (dir) {
    digitalWrite(pin1, HIGH);
    digitalWrite(pin2, LOW);
  } else {
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, HIGH);
  }
}

void fwd_back() {

  set_motor_dir(IN1, IN2, true);
  set_motor_dir(IN3, IN4, true);

  motor_test_speedup_slowdown(5, 100);

  set_motor_dir(IN1, IN2, false);
  set_motor_dir(IN3, IN4, false);
  
  motor_test_speedup_slowdown(5, 100);

}


void motor_test_speedup_slowdown(int increment, int timeout) {
  int PWM_Value = 0; //PWM value for motor 1 and 2
  
  //Motor 1 and Motor 2 run with gradually increasing speed until Max
  for(PWM_Value = min_pwm_speed; PWM_Value<=max_pwm_speed; PWM_Value+=increment){
    Serial.println(PWM_Value);
    analogWrite(ENA, PWM_Value); //set PWM to Motor 1
    analogWrite(ENB, PWM_Value); //set PWM to Motor 2
    delay(timeout); // 100 milliseconds
  }
  Serial.println(0);
  analogWrite(ENA, 0); //set PWM to Motor 1
  analogWrite(ENB, 0); //set PWM to Motor 2
  delay(timeout); // 100 milliseconds
  
  //Motor 1 and Motor 2 run with gradually descreasing speed until Stop
  for(PWM_Value = max_pwm_speed; PWM_Value>=min_pwm_speed; PWM_Value-=increment){
    Serial.println(PWM_Value);
    analogWrite(ENA, PWM_Value); //set PWM to Motor 1
    analogWrite(ENB, PWM_Value); //set PWM to Motor 2
    delay(timeout); // 100 milliseconds
  }
  Serial.println(0);
  analogWrite(ENA, 0); //set PWM to Motor 1
  analogWrite(ENB, 0); //set PWM to Motor 2
  delay(timeout); // 100 milliseconds
}

// BTS7960 Datasheet
// https://www.handsontec.com/dataspecs/module/BTS7960%20Motor%20Driver.pdf
// Upload the following sketch to Arduino board. Try to turn the potentiometer 
// clock-wise and anti-clock-wise and observe how the motor turn.
/*==========================================================================
// Author : Handson Technology
// Project : BTD7960 Motor Control Board driven by Arduino.
// Description : Speed and direction controlled by a potentiometer attached
// to analog input A0. One side pin of the potentiometer (either one) to
// ground; the other side pin to +5V
// Source-Code : BTS7960.ino
// Program: Control DC motors using BTS7960 H Bridge Driver.
//==========================================================================
// Connection to the BTS7960 board:
// BTS7960 Pin 1 (RPWM) to Arduino pin 5(PWM)
// BTS7960 Pin 2 (LPWM) to Arduino pin 6(PWM)
// BTS7960 Pin 3 (R_EN), 4 (L_EN), 7 (VCC) to Arduino 5V pin
// BTS7960 Pin 8 (GND) to Arduino GND
// BTS7960 Pin 5 (R_IS) and 6 (L_IS) not connected
*/

int SENSOR_PIN = 0; // analog 0 pin of the (fake) potentiometer
int RPWM_Output = 5; // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int LPWM_Output = 6; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)

void setup() {
  pinMode(RPWM_Output, OUTPUT);
  pinMode(LPWM_Output, OUTPUT);
}

void loop() {
  // sensor value is in the range 0 to 1023
  int sensorValue = analogRead(SENSOR_PIN);
  
  if (sensorValue < 512) { // reverse rotation
    int reversePWM = -(sensorValue - 511) / 2;
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, reversePWM);
  } else { // forward rotation
    int forwardPWM = (sensorValue - 512) / 2;
    analogWrite(LPWM_Output, forwardPWM);
    analogWrite(RPWM_Output, 0);
  }
}

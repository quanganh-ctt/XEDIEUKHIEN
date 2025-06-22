#include <Arduino.h>
#include "MotorDriver.h"
#include "RobotController.h"
#include <SoftwareSerial.h>

const int IN1 = 6;
const int IN2 = 7;
const int IN3 = 8;
const int IN4 = 9;
const int ENA = 5;
const int ENB = 10;
const int TRIG = 18;
const int ECHO = 19;
const int BT_RX = 4;
const int BT_TX = 3;
const int SPEED = 150;

SoftwareSerial HC05(BT_RX, BT_TX);
MotorDriver motor(IN1, IN2, IN3, IN4, ENA, ENB);
RobotController robot(motor, HC05, TRIG, ECHO, SPEED);

void setup() {
    robot.begin();
}

void loop() {
    robot.checkObstacle();
    robot.control();
}

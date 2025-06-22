#ifndef ROBOTCONTROLLER_H
#define ROBOTCONTROLLER_H

#include <Arduino.h>
#include <SoftwareSerial.h>
#include "MotorDriver.h"

class RobotController {
private:
    MotorDriver& motor;
    SoftwareSerial& bt;
    int trigPin, echoPin;
    int speed;
    bool warning;

public:
    RobotController(MotorDriver& m, SoftwareSerial& b, int trig, int echo, int spd);
    void begin();
    void checkObstacle();
    void control();
};

#endif

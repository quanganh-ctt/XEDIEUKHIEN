#ifndef MOTORDRIVER_H
#define MOTORDRIVER_H

#include <Arduino.h>

class MotorDriver {
private:
    int IN1, IN2, IN3, IN4, ENA, ENB;

public:
    MotorDriver(int in1, int in2, int in3, int in4, int ena, int enb);
    void begin(int speed);
    void moveForward();
    void moveBackward();
    void turnLeft();
    void turnRight();
    void forwardLeft();
    void forwardRight();
    void backwardLeft();
    void backwardRight();
    void stop();
};

#endif
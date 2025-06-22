#include "RobotController.h"

RobotController::RobotController(MotorDriver& m, SoftwareSerial& b, int trig, int echo, int spd)
    : motor(m), bt(b), trigPin(trig), echoPin(echo), speed(spd), warning(false) {}

void RobotController::begin() {
    motor.begin(speed);
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    bt.begin(9600);
    Serial.begin(9600);
}

void RobotController::checkObstacle() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH);
    int distance = duration * 0.034 / 2;
    if (distance < 15) {
        warning = true;
        motor.stop();
        Serial.println("AUTO STOP: Distance too close!");
    } else {
        warning = false;
    }
}

void RobotController::control() {
    if (bt.available()) {
        char cmd = bt.read();
        Serial.println(cmd);
        if (warning && (cmd == 'F' || cmd == 'I' || cmd == 'G')) {
            motor.stop();
            return;
        }

        switch (cmd) {
            case 'F': motor.moveForward(); break;
            case 'B': motor.moveBackward(); break;
            case 'L': motor.turnLeft(); break;
            case 'R': motor.turnRight(); break;
            case 'I': motor.forwardRight(); break;
            case 'G': motor.forwardLeft(); break;
            case 'J': motor.backwardRight(); break;
            case 'H': motor.backwardLeft(); break;
            case 'S': motor.stop(); break;
        }
    }
}
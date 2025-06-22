#include <SoftwareSerial.h>

// ======= Class MotorDriver =======
class MotorDriver {
  int IN1, IN2, IN3, IN4, ENA, ENB;

public:
  MotorDriver(int in1, int in2, int in3, int in4, int ena, int enb)
    : IN1(in1), IN2(in2), IN3(in3), IN4(in4), ENA(ena), ENB(enb) {}

  void begin(int speed) {
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(ENB, OUTPUT);
    analogWrite(ENA, speed);
    analogWrite(ENB, speed);
  }

  void moveForward() {
    digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  }

  void moveBackward() {
    digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  }

  void turnLeft() {
    digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  }

  void turnRight() {
    digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  }

  void forwardLeft() {
    digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  }

  void forwardRight() {
    digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  }

  void backwardLeft() {
    digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  }

  void backwardRight() {
    digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  }

  void stop() {
    digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  }
};

// ======= Class UltrasonicSensor =======
class UltrasonicSensor {
  int trigPin, echoPin;

public:
  UltrasonicSensor(int trig, int echo) : trigPin(trig), echoPin(echo) {}

  void begin() {
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
  }

  int readDistance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH);
    int distance = duration * 0.034 / 2;
    return distance;
  }
};

// ======= Class RobotController =======
class RobotController {
  MotorDriver& motor;
  UltrasonicSensor& sensor;
  SoftwareSerial& bt;
  int speed;
  bool warning;

public:
  RobotController(MotorDriver& m, UltrasonicSensor& s, SoftwareSerial& b, int spd)
    : motor(m), sensor(s), bt(b), speed(spd), warning(false) {}

  void begin() {
    motor.begin(speed);
    sensor.begin();
    bt.begin(9600);
    Serial.begin(9600);
  }

  void checkObstacle() {
    int distance = sensor.readDistance();
    if (distance < 15) {
      warning = true;
      motor.stop();
      Serial.println("AUTO STOP: Distance too close!");
    } else {
      warning = false;
    }
  }

  void control() {
    if (bt.available()) {
      char cmd = bt.read();
      Serial.println(cmd);
      if (warning && (cmd == 'F' || cmd == 'I' || cmd == 'G')) {
        motor.stop();  // Không cho tiến nếu gần vật
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
};

// ======= Global Object Initialization =======
SoftwareSerial HC05(4, 3);
MotorDriver motor(6, 7, 8, 9, 5, 10);
UltrasonicSensor ultrasonic(18, 19);
RobotController robot(motor, ultrasonic, HC05, 150);

// ======= Arduino Setup & Loop =======
void setup() {
  robot.begin();
}

void loop() {
  robot.checkObstacle();
  robot.control();
}

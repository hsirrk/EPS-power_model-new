#ifndef STEPPER_MOTOR_HPP
#define STEPPER_MOTOR_HPP

#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_mac.h"

class StepperMotor {
private:
    gpio_num_t pinList[4];  // Array to store GPIO pins
    int currentPos;         // Current step position
    int fullRevRotations;   // Steps per revolution
    int speed;              // Steps per second

public:
    StepperMotor(gpio_num_t* listOfPins, int numRotations, int speed);
    void rotateTo(int angle);
    void step(int steps);
    float getAngle();
    int currentPosition();
    int getCounts(int angle);
    void writeState(bool states[4]);
    void stop();
};

#endif // STEPPER_MOTOR_HPP

#include "stepperMotor.hpp"
#include "esp_log.h"

// Constructor
StepperMotor::StepperMotor(gpio_num_t* listOfPins, int numRotations, int speed) {
    for (int i = 0; i < 4; i++) {
        this->pinList[i] = listOfPins[i];

        gpio_config_t io_conf = {};
        io_conf.intr_type = GPIO_INTR_DISABLE;
        io_conf.mode = GPIO_MODE_OUTPUT;
        io_conf.pin_bit_mask = (1ULL << this->pinList[i]);
        io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
        io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
        gpio_config(&io_conf);
    }

    this->currentPos = 0;
    this->fullRevRotations = numRotations;
    this->speed = speed;
}

float StepperMotor::getAngle() {
    return (float)this->currentPos / this->fullRevRotations * 360.0f;
}

int StepperMotor::getCounts(int angle) {
    return (angle * this->fullRevRotations) / 360;
}

void StepperMotor::writeState(bool states[4]) {
    for (int i = 0; i < 4; i++) {
        gpio_set_level(this->pinList[i], states[i] ? 1 : 0);
    }
}

void StepperMotor::step(int steps) {
    int dir = (steps >= 0) ? 1 : -1;
    steps = abs(steps);

    bool stepSequence[4][4] = {
        {1, 0, 1, 0}, {0, 1, 1, 0}, {0, 1, 0, 1}, {1, 0, 0, 1}
    };

    for (int i = 0; i < steps; i++) {
        int stepIndex = (this->currentPos % 4 + 4) % 4;
        this->writeState(stepSequence[stepIndex]);

        this->currentPos += dir;
        if (this->currentPos >= this->fullRevRotations) {
            this->currentPos = 0;
        } else if (this->currentPos < 0) {
            this->currentPos = this->fullRevRotations - 1;
        }

        vTaskDelay(10 / this->speed / portTICK_PERIOD_MS);
    }
}

void StepperMotor::rotateTo(int angle) {
    int targetSteps = this->getCounts(angle);
    int stepsToMove = targetSteps - this->currentPos;
    this->step(stepsToMove);
}

void StepperMotor::stop() {
    ;
}

int StepperMotor::currentPosition() {
    return this->currentPos;
}

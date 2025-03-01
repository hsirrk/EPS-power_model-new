#include "stepperMotor.hpp"


extern "C" int app_main(void) { 
    gpio_num_t motorPins[4] = {GPIO_NUM_17, GPIO_NUM_5, GPIO_NUM_18, GPIO_NUM_19};
    StepperMotor motor(motorPins, 200, 100); // Initialize inside app_main
    while (1) {
        motor.step(1000);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        motor.stop();
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }

    
}
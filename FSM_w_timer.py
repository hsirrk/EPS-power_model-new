"""
This is the FSM file, responsible for managing power consumption in the power model.

It operates based on the provided power consumption dictionary. An action is requested, 
and the FSM checks if it's feasible based on the available power (obtained from the engine).

Input: Function (action name), time spent in state 
Output: Action success/failure,  remaining power and the amount of time spent in every state

Notes: All functionalities consume different power in different states (refer to 
the power consumption dictionary).

            
#Note 2: Cross check the time values for camera and centrifuge
            

"""

import datetime
import time
from Engine_w_timer import (
    get_running_total,
)  # Assuming this retrieves total power available
import random

filepath = r"enter the filepath"

# Define power consumption dictionary (watts)
power_consumption = {
    "ADCS_IDLE": 0.3044,
    "ADCS_ACTUATE": 2,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0.726,
    "CAM_OFF": 0,
    "OBC_LOW_POWER": 0.6,
    "OBC_IDLE": 0.63,
    "COMMS_IDLE": 0.0005,
    "COMMS_RX": 0.0658,
    "COMMS_TX": 3.5632,
    "COMMS_TX_BEACON": 3.562,
    "COMMS_ANT_DEPLOY": 5.05,
    "EPS_IDLE": 0.075,
    "EPS_LOW_POWER": 0.043,
}

# Define percentage of time active for various states
detumbling = {
    "ADCS_IDLE": 79.04,
    "ADCS_ACTUATE": 0.962,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0,
    "CAM_OFF": 100,
    "OBC_LOW_POWER": 0,
    "OBC_IDLE": 100,
    "COMMS_IDLE": 0,
    "COMMS_RX": 0,
    "COMMS_TX": 100,
    "COMMS_TX_BEACON": 0,
    "COMMS_ANT_DEPLOY": 0,
    "EPS_IDLE": 100,
    "EPS_LOW_POWER": 0,
}

# Define seconds active for other states
antenna_deploy = {
    "ADCS_IDLE": 1.67,
    "ADCS_ACTUATE": 0,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0,
    "CAM_OFF": 100,
    "OBC_LOW_POWER": 0,
    "OBC_IDLE": 100,
    "COMMS_IDLE": 0,
    "COMMS_RX": 0,
    "COMMS_TX": 0,
    "COMMS_TX_BEACON": 0,
    "COMMS_ANT_DEPLOY": 15,
    "EPS_IDLE": 100,
    "EPS_LOW_POWER": 0,
}

# Define other states
detumbed_beacon = {
    "ADCS_IDLE": 1.67,
    "ADCS_ACTUATE": 0,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0,
    "CAM_OFF": 100,
    "OBC_LOW_POWER": 0,
    "OBC_IDLE": 100,
    "COMMS_IDLE": 0,
    "COMMS_RX": 0,
    "COMMS_TX": 0,
    "COMMS_TX_BEACON": 100,
    "COMMS_ANT_DEPLOY": 0,
    "EPS_IDLE": 100,
    "EPS_LOW_POWER": 0,
}

idle = {
    "ADCS_IDLE": 79.65,
    "ADCS_ACTUATE": 0.426,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0,
    "CAM_OFF": 100,
    "OBC_LOW_POWER": 0,
    "OBC_IDLE": 100,
    "COMMS_IDLE": 0,
    "COMMS_RX": 0,
    "COMMS_TX": 0,
    "COMMS_TX_BEACON": 540,
    "COMMS_ANT_DEPLOY": 0,
    "EPS_IDLE": 100,
    "EPS_LOW_POWER": 0,
}

low_power = {
    "ADCS_IDLE": 0,
    "ADCS_ACTUATE": 0,
    "ADCS_OFF": 100,
    "CAM_CAPTURE": 0,
    "CAM_OFF": 100,
    "OBC_LOW_POWER": 100,
    "OBC_IDLE": 0,
    "COMMS_IDLE": 100,
    "COMMS_RX": 0,
    "COMMS_TX": 0,
    "COMMS_TX_BEACON": 0,
    "COMMS_ANT_DEPLOY": 0,
    "EPS_IDLE": 0,
    "EPS_LOW_POWER": 100,
}

camera = {
    "ADCS_IDLE": 4291,
    "ADCS_ACTUATE": 23,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 60,
    "CAM_OFF": 5340,
    "OBC_LOW_POWER": 0,
    "OBC_IDLE": 540,
    "COMMS_IDLE": 0,
    "COMMS_RX": 0,
    "COMMS_TX": 0,
    "COMMS_TX_BEACON": 0,
    "COMMS_ANT_DEPLOY": 0,
    "EPS_IDLE": 60,
    "EPS_LOW_POWER": 0,
}

centrifuge = {
    "ADCS_IDLE": 4291,
    "ADCS_ACTUATE": 23,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0,
    "CAM_OFF": 5400,
    "OBC_LOW_POWER": 0,
    "OBC_IDLE": 540,
    "COMMS_IDLE": 0,
    "COMMS_RX": 0,
    "COMMS_TX": 0,
    "COMMS_TX_BEACON": 0,
    "COMMS_ANT_DEPLOY": 0,
    "EPS_IDLE": 300,
    "EPS_LOW_POWER": 0,
}

voltage_consumption = {"Camera_OBC": 3.3, "LPU": 3.3, "Torquers": 5.5}  # volts  # volts

action_state_list = [
    "power_consumption",
    "detumbling",
    "antenna_deploy",
    "detumbed_beacon",
    "idle",
    "low_power",
    "camera",
    "centrifuge",
]
state_time_dict = {}
avg_power_cons = sum(power_consumption.values())  # 16.619899999999998 W


class FSM:
    """
    This class handles action processing for the CubeSat, managing power consumption.
    """

    def __init__(self, battery_capacity=20):
        # Current state of the FSM
        self.battery_capacity = (
            battery_capacity  # Assuming the battery capacity is 20 Wh
        )
        self.action_state = "idle"  # Assuming "idle" is the initial state

    def process_action(
        self, action_name, running_total, action_state_time, avg_power_cons
    ):
        total_energy_consumed = 0
        total_time_spent = 0

        # Check if running total power is greater than average power consumption
        if running_total < avg_power_cons:
            print(
                f"Action '{action_name}' cannot be performed. Running total {running_total:.2f}W is less than average power consumption {avg_power_cons:.2f}W."
            )
            return None, None

        if action_name in ["detumbling", "detumbed_beacon", "idle", "low_power"]:
            total_energy_consumed = running_total * (action_state_time / 3600)
            if total_energy_consumed > self.battery_capacity:
                print(
                    f"Action '{action_name}' cannot be performed. Not enough battery capacity."
                )
                print(running_total)
                return None, None
            total_time_spent = action_state_time

        elif action_name in ["antenna_deploy", "camera", "centrifuge"]:
            total_energy_consumed = running_total * (
                sum(eval(action_name).values()) / 3600
            )
            if total_energy_consumed > self.battery_capacity:
                print(
                    f"Action '{action_name}' cannot be performed. Not enough battery capacity."
                )
                print(running_total)
                return None, None
            total_time_spent = sum(eval(action_name).values())

        else:
            raise ValueError(f"Unknown action name: {action_name}")

        return total_energy_consumed, total_time_spent


# Initialize FSM and retrieve running total
running_total = 18  # get_running_total(filepath)

# Instantiate the FSM
fsm = FSM()

# Calculate average power consumption
avg_power_cons = sum(power_consumption.values())

# Process action based on current running total
action_name = action_state_list[2]
action_state_time = (
    100  # Provide the number of seconds for the actions that work under %seconds
)
energy_consumed, time_spent = fsm.process_action(
    action_name, running_total, action_state_time, avg_power_cons
)

# Check if the action was performed successfully
if energy_consumed is not None and time_spent is not None:
    print(
        f"Total power consumed: {energy_consumed:.2f} Wh, Total time spent doing {action_name}: {time_spent:.2f} seconds"
    )
else:
    print("Action could not be performed due to insufficient battery capacity.")

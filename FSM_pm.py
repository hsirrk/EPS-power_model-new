"""
This is the FSM file, responsible for managing power consumption in the power model.

It operates based on the provided power consumption dictionary. An action is requested, 
and the FSM checks if it's feasible based on the available power (obtained from the engine).

Input: Function (action name), State
Output: Action success/failure and (potentially) remaining power

Notes: All functionalities consume different power in different states (refer to 
the power consumption dictionary).
"""

import datetime
import time

from Engine_pm import get_running_total  # Assuming this retrieves total power available

running_total=get_running_total()


# Power consumption dictionary (watts)
power_consumption = {
    "ADCS_IDLE": 0.3044,
    "ADCS_ACTUATE": 2.0,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0.726,
    "CAM_OFF": 0,
    "OBC_LOW_POWER": 0.6,
    "OBC_IDLE": 0.63,
    "COMMS_IDLE": 0.0005,
    "COMMS_RX": 0.0658,
    "COMMS_TX": 3.5632,
    "COMMS_TX_BEACON": 3.5632,
    "COMMS_ANT_DEPLOY": 5.05,
    "CENT_TEST": 0.2678,
    "CENT_OFF": 0,
    "EPS_IDLE": 0.075,
    "EPS_LOW_POWER": 0.043
}

detumbling = {
    "ADCS_IDLE": 79.04,  # DETUMBLING %_active
    "ADCS_ACTUATE": 0.962,
    "ADCS_OFF": 0,
    "CAM_CAPTURE": 0,
    "CAM_OFF": 0,
    "OBC_LOW_POWER": 100,  # Assuming low power mode is active (100)
    "OBC_IDLE": 0,         # Assuming idle mode is inactive (0)
    "COMMS_IDLE": 0,
    "COMMS_RX": 0,
    "COMMS_TX": 0,
    "COMMS_TX_BEACON": 0,    # Assuming communication is inactive (0)
    "COMMS_ANT_DEPLOY": 0,   # Assuming antenna deployment is inactive (0)
    "CENT_TEST": 0,
    "CENT_OFF": 100,        # Assuming centrifuge is off (100)
    "EPS_IDLE": 0,          # Assuming EPS is not in idle mode (0)
    "EPS_LOW_POWER": 0       # Assuming EPS is not in low power mode (0)
}

voltage_consumption = {
    "Camera_OBC": 3.3, #volts
    "LPU": 3.3, #volts
    "Torquers": 5.5
}



class FSM:

    """
    This class handles action processing for the CubeSat, managing power consumption.
    """

    def __init__(self):
        # Current state of the FSM
        self.state = "idle"  # Assuming "idle" is the initial state
        
        
    def is_action_valid(self, action_name):
        """
        Checks if the requested action is valid based on available power.

        Args:
            action_name (str): The name of the action to be performed.

        Returns:
            bool: True if the action is valid (enough power), False otherwise.
        """

        return (running_total) >= power_consumption[action_name]
    def process_action(self, action_name, state, running_total):
      
      """
        Attempts to process the requested action, checking power availability and updating state/power.

        Args:
            action_name (str): The name of the action to be performed.
            state (str): The current state of the FSM.

        Returns:
            str: "Action successful" if valid, "Insufficient power" otherwise.
      """

      if self.is_action_valid(action_name):
        
        # Update running total with power consumption
        running_total -= power_consumption[action_name]
        self.state = state  # Update state if needed

        return "Action successful"
      else:
          return "Insufficient power for action"

# Example usage (replace with your integration)
action = "ADCS_ACTUATE"
new_state = "active"  # Assuming action changes state

fsm = FSM()  # Replace with your engine object
result = fsm.process_action(action, new_state, running_total)

print(result)  # Should print "Action successful" or "Insufficient power for action"

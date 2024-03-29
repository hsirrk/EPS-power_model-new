"""
This is the FSM file, responsible for managing power consumption in the power model.

It operates based on the provided power consumption dictionary. An action is requested, 
and the FSM checks if it's feasible based on the available power (obtained from the engine).

Input: Function (action name), time spent in state 
Output: Action success/failure,  remaining power and the amount of time spent in every state

Notes: All functionalities consume different power in different states (refer to 
the power consumption dictionary).


"""

import datetime
import time
from Engine_pm import get_running_total  # Assuming this retrieves total power available

filepath=r"Enter the filepath"

running_total=get_running_total(filepath)
state_time=0


# Power consumption dictionary (watts)
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

detumbling = { #%_active

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


antenna_deploy = { #sec_active

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


detumbed_beacon = { #%_active

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

idle = { #%_active

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


low_power = { #%_active

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


camera = { #sec_active

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


centrifuge = { #sec_active

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


voltage_consumption = {
    "Camera_OBC": 3.3, #volts
    "LPU": 3.3, #volts
    "Torquers": 5.5
}

action_state_list=["detumbling", "antenna_deploy" , "detumbed_beacon", "idle", "low_power", "camera", "centrifuge"]
state_time_dict={}



class FSM:

    """
    This class handles action processing for the CubeSat, managing power consumption.
    """

    def __init__(self):
        # Current state of the FSM
        self.action_state = "idle"  # Assuming "idle" is the initial state
        
        
    def is_action_valid(self, action_name):
        """
        Checks if the requested action is valid based on available power.

        Args:
            action_name (str): The name of the action to be performed.

        Returns:
            bool: True if the action is valid (enough power), False otherwise.
        """

        return running_total >= power_consumption[action_name]
    def process_action(self, action_name,running_total):
      
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
        running_total = running_total-power_consumption[action_name]

        return running_total
      else:
          return "Insufficient power for action"
    
    def process_action_state(self,action_name,action_state_time):
        
        
        for action_state in action_state_list:
            if action_state=="antenna_deploy":
                state_time=antenna_deploy[action_name]
                state_time_dict[action_state]=state_time
        
            elif action_state=="camera":
                state_time=camera[action_name]
                state_time_dict[action_state]=state_time
        
            elif action_state=="centrifuge":
                state_time=centrifuge[action_name]
                state_time_dict[action_state]=state_time
            
            elif action_state=="detumbling":
                state_time=action_state_time*detumbling[action_name]/100
                state_time_dict[action_state]=state_time
            
            elif action_state=="detumbed_beacon":
                state_time=action_state_time*detumbed_beacon[action_name]/100
                state_time_dict[action_state]=state_time
            
            elif action_state=="idle":
                state_time=action_state_time*idle[action_name]/100
                state_time_dict[action_state]=state_time
            
            elif action_state=="low_power":
                state_time=action_state_time*low_power[action_name]/100
                state_time_dict[action_state]=state_time
 
            

# Example usage (replace with your integration)
action_name = "EPS_LOW_POWER" # enter the action that needs to be performed
action_state_time= 100 # enter the total time spent in the state

fsm = FSM()  
result = fsm.process_action(action_name, running_total)
state_time=fsm.process_action_state(action_name,action_state_time)


if result=="Insufficient power for action":
    print(result)
else:
    print(f"Action completed, Power remaining: {result} W")

    
for key, value in state_time_dict.items():
    print(f'{key}:{value} Sec')

import datetime
import time
from Engine_w_timer import get_running_total  # Assuming this retrieves total power available

filepath = r"D:\krish\Documents\UBC year 3\UBC orbit\New_power_model\Power_Generation.csv"



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

detumbling = { #%sec_active

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


detumbed_beacon = { #%sec_active

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

idle = { #%sec_active

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


low_power = { #%sec_active

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

action_state_list=["power_consumption","detumbling", "antenna_deploy" , "detumbed_beacon", "idle", "low_power", "camera", "centrifuge"]
state_time_dict={}


class FSM:
    """
    This class handles action processing for the CubeSat, managing power consumption.
    """

    def __init__(self, battery_capacity=40):
        # Current state of the FSM
        self.battery_capacity = battery_capacity  # Assuming the battery capacity is 40 Wh
        self.action_state = "idle"  # Assuming "idle" is the initial state

    def process_action(self, action_name, running_total, action_state_time):
        
        total_energy_consumed=running_total*(action_state_time/3600)
    
        if total_energy_consumed > self.battery_capacity:   
            print(f"Action '{action_name}' cannot be performed. Not enough battery capacity.")
            print(running_total)
            return None
        if action_name == "power_consumption":
            total_power_consumed = 0
            for key, value in power_consumption.items():
                total_power_consumed += value
            return running_total - total_power_consumed

        elif action_name == "antenna_deploy":
            total_time_spent = sum(antenna_deploy.values())
            return total_time_spent

        elif action_name == "camera":
            total_time_spent = sum(camera.values())
            return total_time_spent

        elif action_name == "centrifuge":
            total_time_spent = sum(centrifuge.values())
            return total_time_spent

        elif action_name in ["detumbling", "detumbed_beacon", "idle", "low_power"]:
            total_time_spent = 0
            if action_name == "detumbling":
                total_time_spent = sum(detumbling.values()) * action_state_time / 100
            elif action_name == "detumbed_beacon":
                total_time_spent = sum(detumbed_beacon.values()) * action_state_time / 100
            elif action_name == "idle":
                total_time_spent = sum(idle.values()) * action_state_time / 100
            elif action_name == "low_power":
                total_time_spent = sum(low_power.values()) * action_state_time / 100

            return total_time_spent

        else:
            raise ValueError(f"Unknown action name: {action_name}")

# Initialize FSM and retrieve running total
running_total = get_running_total(filepath)

# Instantiate the FSM
fsm = FSM()

# Process each action state
for action_name in action_state_list:
    action_state_time = 100  # Example time spent in each state, you should adjust this as per your scenario

    # Process action based on current running total
    result = fsm.process_action(action_name, running_total, action_state_time)

    if action_name == "power_consumption":
        print(f"Total power consumed is {result:.2f} Watts")
    else:
        print(f"Total time spent doing {action_name} is {result:.2f} seconds")

    print(f"Current running total: {running_total:.2f}")

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

filepath = r"D:\krish\Documents\UBC year 3\UBC orbit\New_power_model\Alea_Solar_Panel_Power (2).csv"

running_total=get_running_total(filepath)
state_time=0
#x=16.619899999999998
l1=[] # list to track the time spent in each "functionality"

    


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

action_state_list=["detumbling", "antenna_deploy" , "detumbed_beacon", "idle", "low_power", "camera", "centrifuge"]
state_time_dict={}

def get_total_power_cons():
    sum=0
    for key,value in power_consumption.items():
        sum=sum+value
    return sum

class FSM:

    """
    This class handles action processing for the CubeSat, managing power consumption.
    """

    def __init__(self):
        # Current state of the FSM
        self.action_state = "idle"  # Assuming "idle" is the initial state
    
    def process_action(self, action_name,running_total, action_state_time):     
        
        x=get_total_power_cons()
        if action_name == "power_consumption":
            return running_total-x
        
        if action_name=="antenna_deploy":
            sum=0
            for key,value in antenna_deploy.items():
                sum=sum+value
                print("time spent in",key,"is:",value)
            return sum
        if action_name=="camera":
            sum=0
            for key,value in camera.items():
                sum=sum+value
                print("time spent in",key,"is:",value)
            return sum
        if action_name=="centrifuge":
            sum=0
            for key,value in centrifuge.items():
                sum=sum+value
                print("time spent in",key,"is:",value)
            return sum
        
        if action_name=="detumbling":
            sum=0
            for key,value in detumbling.items():
                sum=sum+value*action_state_time/100
                print("time spent in",key,"is:",value*action_state_time/100)
            return sum
        if action_name=="detumbed_beacon":
            sum=0
            for key,value in detumbed_beacon.items():
                sum=sum+value*action_state_time/100
                print("time spent in",key,"is:",value*action_state_time/100)
            return sum
        if action_name=="idle":
            sum=0
            for key,value in idle.items():
                sum=sum+value*action_state_time/100
                print("time spent in",key,"is:",value*action_state_time/100)
            return sum
        if action_name=="low_power":
            sum=0
            for key,value in low_power.items():
                sum=sum+value*action_state_time/100
                print("time spent in",key,"is:",value*action_state_time/100)
            return sum
                
                
            

for action in action_state_list:
    action_name = action # enter the action that needs to be performed
    action_state_time= 100 # enter the total time spent in the state

    fsm = FSM()  
    result = fsm.process_action(action_name, running_total,action_state_time)


    if action_name=="power_consumption":
        print("Total power consumed is",result,"Watts")
    else:
        print("Total time spent doing task is",result,"seconds")
    print(running_total)
    

    
    
        
        
    

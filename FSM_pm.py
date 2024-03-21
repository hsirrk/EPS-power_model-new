"""
  This is the FSM file, it is responsible for the consumption in the power model. 
  
  It operates based on the FSM diagram.
  
  An action has to be requested to the power model, if the model deems the action to be doable based on the total power avaliable, the action gets perfromed. 


things to work on:

create a safe mode
check power availability based on the power genereated(made by the engine file)
make low power mode work
create a dictionary to store all the power consumption values for each action
"""
import datetime
import time

" The dictonary below shows the actions as keys and the respective power consumption(watts) as their value"
power_consumption = {
  "ADCS_IDLE": 0.3044,  # Watts
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

voltage_consumption = {
    "Camera_OBC": 3.3, #volts
    "LPU": 3.3, #volts
    "Torquers": 5.5
}

class FSM:
  """
  This class handles action processing for the CubeSat.
  """

  def __init__(self, engine):
    # Current state of the FSM
    self.state = "idle"  # Assuming "idle" is the initial state

    # Reference to the engine object for power availability checks
    self.engine = engine

  def process_action(self, action_name, duration):
    """
    Processes an action based on the current state and power availability.

    This function checks if the action is valid in the current state, 
    if there's enough power to perform it, and then executes the action 
    (state transition and battery level update) if both conditions are met.

    Args:
      action_name (str): The name of the action to be performed.
      duration (float): The duration (in seconds) for which to perform the action.

    Raises:
      Exception: If the action is invalid for the current state or power is insufficient.
    """

    # Check if action is valid in the current state
    if self.is_valid_action(action_name):
      # Check power availability before performing the action
      if self.engine.is_action_feasible(datetime.datetime.now(), action_name, duration):
        self._execute_action(action_name, duration)
      else:
        raise Exception("Insufficient power to perform action")
    else:
      raise Exception(f"Invalid action '{action_name}' for state '{self.state}'")
      
  def is_valid_action(self, action_name):
    """
    Checks if the action is allowed based on the current state.

    This function implements the FSM logic to determine if an action is valid 
    in the current state, considering additional states and power constraints.

    Args:
      action_name (str): The name of the action to be checked.

    Returns:
      bool: True if the action is valid, False otherwise.
    """

    if self.state == "idle":
      if action_name == "orientation_command":
        self.state = "detumbling"
        return True
      elif action_name == "picture_command":
        self.state = "camera"
        return True
    elif self.state == "detumbling":
      if action_name == "complete_detumbling":  # Assuming this completes detumbling
        self.state = "idle"
        return True
    elif self.state == "camera":
      if action_name == "picture_captured":
        # Check power availability before taking a picture
        if self.engine.is_action_feasible(datetime.datetime.now(), action_name):
          self.state="idle"
          return True
        else:
          print("Insufficient power to take picture. Entering low_power state.")
          self.state = "low_power"
          return False
    elif self.state == "low_power":
      # Limited actions allowed in low power state (e.g., centrifuge for momentum control)
      if action_name == "centrifuge":
        # Check power availability before using centrifuge
        if self.engine.is_action_feasible(datetime.datetime.now(), action_name):
          return True
        else:
          print("Insufficient power to use centrifuge. Staying in low_power state.")
          return False
      # If ground pass detection is implemented, add logic here to transition to other states
      # based on communication opportunities during ground pass
      # elif action_name == "ground_pass":  # Assuming this indicates ground pass detection
      #   # ... transition logic based on ground pass information ...
      #   return True
    else:
      raise Exception(f"Invalid state encountered: {self.state}")  # Handle unexpected states

    return False  # Action not valid in the current state





  def _execute_action(self, action_name, duration):
    """
    Executes the action, updates the state, and battery level.

    This function performs the actual action (e.g., taking a picture), 
    updates the state of the FSM, and calls the engine to update the battery level 
    based on the action's power consumption.

    Args:
      action_name (str): The name of the action to be performed.
      duration (float): The duration (in seconds) for which to perform the action.
    """
    # Simulate action execution (replace with actual action code)
    time.sleep(duration)  # Replace with actual execution logic
    print(f"Action '{action_name}' completed")

    # Update state (implement logic based on action and FSM)
    # ...

    # Update battery level based on power consumption
    self.engine.update_battery_level(datetime.datetime.now(), action_name, duration)

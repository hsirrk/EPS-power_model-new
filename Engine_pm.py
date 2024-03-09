import datetime

class Engine:
  """
  This class manages power prediction, consumption, and availability for the CubeSat.
  """

  def __init__(self, solar_panel_data, orbit_data, power_consumption_models):
    # Solar panel properties
    self.solar_panel_data = solar_panel_data  # Dictionary with panel efficiency etc.

    # Orbit data for simulation (e.g., ECI positions, orbital parameters)
    self.orbit_data = orbit_data

    # Power consumption models for different functions and commands
    self.power_consumption_models = power_consumption_models  # Dictionary with functions

    # Initial battery level
    self.battery_level = 0.0

    # Error margin for power calculations
    self.error_margin = 0.1  # Adjust this value as needed

  def set_initial_battery_level(self, level):
    """
    Sets the initial battery level of the CubeSat.

    Args:
      level (float): The initial battery level in Wh or similar units.
    """
    self.battery_level = level

  def get_predicted_power(self, time):
    """
    Predicts the power generation at a specific time based on orbit data.

    This function uses the satellite's ECI position (from orbit_data) 
    and solar panel properties to estimate power generation at the given time.

    Args:
      time (datetime.datetime): The time for which to predict power generation.

    Returns:
      float: The predicted power generation at the given time (in Watts).
    """
    # Extract ECI position from orbit_data for the given time
    eci_position = self.get_eci_position(time)

    # Use ECI position and solar panel data to estimate solar irradiance
    solar_irradiance = self.calculate_solar_irradiance(eci_position)

    # Calculate power generation based on solar irradiance and panel efficiency
    generated_power = self.solar_panel_data['efficiency'] * solar_irradiance

    return generated_power

  def calculate_power_consumption(self, action_name, duration):
    """
    Calculates the power consumption for a specific action.

    This function uses the provided power consumption models to estimate 
    the total power consumed by the action during the specified duration.

    Args:
      action_name (str): The name of the action to be performed.
      duration (float): The duration (in seconds) for which to calculate power consumption.

    Returns:
      float: The total power consumption for the action (in Wh).
    """
    if action_name in self.power_consumption_models:
      consumption_model = self.power_consumption_models[action_name]
      consumed_power = consumption_model(duration)
    else:
      raise Exception(f"Power consumption model not found for action '{action_name}'")

    return consumed_power

  def is_action_feasible(self, time, action_name, duration):
    """
    Checks if there's enough power to perform an action at a specific time.

    This function considers the predicted power generation, current battery level, 
    and power consumption of the action to determine feasibility.

    Args:
      time (datetime.datetime): The time at which the action is planned.
      action_name (str): The name of the action to be performed.
      duration (float): The duration (in seconds) of the action.

    Returns:
      bool: True if the action is feasible, False otherwise.
    """
    predicted_power = self.get_predicted_power(time)
    predicted_consumption = self.calculate_power_consumption(action_name, duration)

    # Consider error margin and check if available power is sufficient
    available_power = predicted_power * (1 + self.error_margin) + self.battery_level
    is_feasible = available_power > predicted_consumption

    return is_feasible

  def update_battery_level(self, time, action_name, duration):
    """
    Updates the battery level after performing an action.

    This function subtracts the power consumption of the action from the 
    current battery level and updates the internal state.

    Args:
      time (datetime.datetime): The time at which the action is performed.
      action_name (str): The name of the action performed.
      duration (float)
      
    """
    
    

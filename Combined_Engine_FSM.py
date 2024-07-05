import pandas as pd
import schedule
import time
from datetime import datetime


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

detumbling = {  # %sec_active
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


antenna_deploy = {  # sec_active
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


detumbed_beacon = {  # %sec_active
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

idle = {  # %sec_active
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


low_power = {  # %sec_active
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


camera = {  # sec_active
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


centrifuge = {  # sec_active
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


class SolarPowerModel:
    def __init__(self, filepath, time_column="Time (UTCG)", power_column="Power (W)"):
        self.filepath = filepath
        self.time_column = time_column
        self.power_column = power_column
        self.current_row = 0
        self.running_total = 0

    def process_csv_data(self):
        try:
            data = pd.read_csv(self.filepath)
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return None
        except pd.errors.ParserError as e:
            print(f"Error: Parsing error in CSV - {e}")
            return None

        if not (self.time_column in data.columns and self.power_column in data.columns):
            print(
                f"Error: Columns '{self.time_column}' and '{self.power_column}' not found in CSV"
            )
            return None

        data[self.power_column] = pd.to_numeric(
            data[self.power_column], errors="coerce"
        )
        data = data.dropna(subset=[self.power_column])

        return data[[self.time_column, self.power_column]]

    def read_one_row(self):
        solar_data = self.process_csv_data()
        if solar_data is None:
            return

        if self.current_row < len(solar_data):
            row = solar_data.iloc[self.current_row]
            solar_power = float(row[self.power_column])
            time_value = row[self.time_column]

            self.running_total += solar_power

            print(
                f"Time: {time_value}, Solar Power: {solar_power} W, running total = {self.running_total}"
            )

            self.current_row += 1
        else:
            print("No more data to read")

    def schedule_reading(self):
        schedule.every(1).seconds.do(self.read_one_row)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def main(self):
        self.schedule_reading()


def get_running_total(filepath, time_column="Time (UTCG)", power_column="Power (W)"):
    model = SolarPowerModel(filepath, time_column, power_column)
    model.main()  # Start reading data
    return model.running_total


class FSM:
    def __init__(self, battery_capacity=40):
        self.battery_capacity = battery_capacity
        self.action_state = "idle"

    def process_action(self, action_name, running_total, action_state_time):
        total_energy_consumed = running_total * (action_state_time / 3600)

        if total_energy_consumed > self.battery_capacity:
            print(
                f"Action '{action_name}' cannot be performed. Not enough battery capacity."
            )
            return None

        if action_name == "power_consumption":
            total_power_consumed = sum(power_consumption.values())
            return running_total - total_power_consumed

        elif action_name in ["detumbling", "detumbed_beacon", "idle", "low_power"]:
            total_time_spent = 0
            if action_name == "detumbling":
                total_time_spent = sum(detumbling.values()) * action_state_time / 100
            elif action_name == "detumbed_beacon":
                total_time_spent = (
                    sum(detumbed_beacon.values()) * action_state_time / 100
                )
            elif action_name == "idle":
                total_time_spent = sum(idle.values()) * action_state_time / 100
            elif action_name == "low_power":
                total_time_spent = sum(low_power.values()) * action_state_time / 100

            return total_time_spent

        else:
            raise ValueError(f"Unknown action name: {action_name}")


if __name__ == "__main__":
    filepath = r"C:\Users\berty\OneDrive\Documents\UBC\Design Teams\UBC Orbit\EPS-power_model-new\Power_Generation.csv"
    running_total = get_running_total(filepath)
    fsm = FSM()
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

    for action_name in action_state_list:
        action_state_time = 100  # Example time spent in each state, adjust as needed
        result = fsm.process_action(action_name, running_total, action_state_time)

        if action_name == "power_consumption":
            print(f"Total power consumed is {result:.2f} Watts")
        else:
            print(f"Total time spent doing {action_name} is {result:.2f} seconds")

        print(f"Current running total: {running_total:.2f}")

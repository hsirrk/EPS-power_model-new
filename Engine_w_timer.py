"""
This is the engine file for the power model, it keeps track of the power generated by the solar panels

Input: the CSV data (currently)

Output: the power generated on a timely basis (updates every 2 mins)

"""
import pandas as pd
import schedule
import time

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
            print(f"Error: Columns '{self.time_column}' and '{self.power_column}' not found in CSV")
            return None

        # Ensure the power column is numeric
        data[self.power_column] = pd.to_numeric(data[self.power_column], errors='coerce')

        # Drop rows with non-numeric values in the power column
        data = data.dropna(subset=[self.power_column])

        return data[[self.time_column, self.power_column]]

    def read_one_row(self):
        solar_data = self.process_csv_data()
        if solar_data is None:
            return

        # Check if there are more rows to read
        if self.current_row < len(solar_data):
            # Read the current row
            row = solar_data.iloc[self.current_row]
            # Process the row as needed
            solar_power = float(row[self.power_column])  # Convert to float
            time_value = row[self.time_column]

            # Update the running total
            self.running_total += solar_power

            # Print the current row's data
            print(f"Time: {time_value}, Solar Power: {solar_power} W, running total = {self.running_total}")

            # Move to the next row
            self.current_row += 1
        else:
            print("No more data to read")

    def schedule_reading(self):
        # Schedule the task to run every 1 seconds
        schedule.every(1).seconds.do(self.read_one_row)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def main(self):
        self.schedule_reading()

    def get_running_total(self):
        running_total = 0  # Reset running total to 0
        solar_data = self.process_csv_data()
        if solar_data is None:
            return

        for index, row in solar_data.iterrows():
            solar_power = row[self.power_column]
            running_total += solar_power

        return running_total

def get_running_total(filepath, time_column="Time (UTCG)", power_column="Power (W)"):
    model = SolarPowerModel(filepath, time_column, power_column)
    return model.get_running_total()

if __name__ == "__main__":
    filepath = r"D:\krish\Documents\UBC year 3\UBC orbit\New_power_model\Power_Generation.csv"
    model = SolarPowerModel(filepath)
    model.main()



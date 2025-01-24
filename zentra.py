import pandas as pd
from pprint import pprint
import sys, os

input_folder = r'input_data/zentra_data'
output_folder = r'output_data/zentra'

output_file = os.path.join(output_folder, 'zentra_postgres.csv')

# Check if the output file exists, and if it does, remove it
if os.path.exists(output_file):
    os.remove(output_file)
    pprint(f"Existing file {output_file} has been removed.")
else:
    pprint(f"No existing file found. Creating a new one.")

first_file = True  # Flag to handle the header for the first file
for subdir, dirs, files in os.walk(input_folder):
    for file in files:
        if file.startswith('zentra') and file.endswith('.xlsx'):
            df = pd.read_excel(os.path.join(input_folder, file), skiprows=[0, 1])
            
            # Renaming columns for clarity
            df.rename(columns={
                'Timestamp': 'timestamp',
                ' m³/m³ Water Content': 'h2o_content',
                ' °C Soil Temperature': 'soil_temp',
                ' mS/cm Bulk EC': 'elec_conduct',
                '° Wind Direction': 'wind_dir',
                ' m/s Wind Speed': 'wind_sp',
                ' m/s Gust Speed': 'gust_sp',
                ' °C Anemometer Temp': 'anemo_air_temp',
                '° X-axis Level': 'x_axis',
                '° Y-axis Level': 'y_axis',
                ' °C Air Temperature': 'air_temp',
                ' RH Relative Humidity': 'rel_hum',
                ' kPa Atmospheric Pressure': 'atm_press',
                '% Battery Percent': 'batt_percent',
                ' mV Battery Voltage': 'batt_volt'
            }, inplace=True)
            
            # Formatting timestamp
            df['timestamp'] = df['timestamp'].dt.strftime('%Y%m%d %H:%M:%S')
            
            # Exporting data to CSV, appending data after the first file
            df.to_csv(
                os.path.join(output_file),
                sep=',',
                index=False,
                mode='a',  # 'a' for append mode
                header=first_file  # Write header only for the first file
            )
            
            # After processing the first file, set the flag to False so that headers are not written again
            first_file = False
            
            pprint(f"Exporting file {file}.")
        else:
            pprint(f"{file} is not a Zentra data file.")

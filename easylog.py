import os
import pandas as pd
from pprint import pprint

input_folder = r'input_data/easylog_data'
output_folder = r'output_data/easylog'

output_file = os.path.join(output_folder, 'easylog_postgres.csv')

# Check if the output file exists, and if it does, remove it
if os.path.exists(output_file):
    os.remove(output_file)
    pprint(f"Existing file {output_file} has been removed.")
else:
    pprint(f"No existing file found. Creating a new one.")

# Initialize a flag to handle the header
first_file = True

for subdir, dirs, files in os.walk(input_folder):
    for file in files:
        if file.startswith('ELOG') and file.endswith('.TXT'):
            # Read and process the file
            data = pd.read_fwf(os.path.join(input_folder, file), colspecs=[(0,19), (24,30), (32,39), (39,49)])
            df = data.drop(index=[0, 1, 2, 3]).reset_index(drop=True)
            #pprint(df)

            df['timestamp'] = pd.to_datetime(df['#Name EasyLog034'], format='%d.%m.%Y %H:%M:%S')
            df['timestamp'] = df['timestamp'].dt.strftime('%Y%m%d %H:%M:%S')
            df.drop('#Name EasyLog034', axis=1, inplace=True)
     
            
            df.rename(columns={'Unnamed: 1': 'air_temp'}, inplace=True)
            df.rename(columns={'Unnamed: 2': 'vbatt'}, inplace=True)
            df.rename(columns={'Unnamed: 3': 'in_radiation'}, inplace=True)
            df = df[['timestamp', 'air_temp', 'in_radiation', 'vbatt']]
            #pprint(df)
            # Write to CSV, append if not the first file
            df.to_csv(
                os.path.join(output_file),
                sep=',',
                index=False,
                mode='a',
                header=first_file  # Write header only for the first file
            )
            # After processing the first file, set the flag to False
            first_file = False
            pprint(f"Exporting file {file}.")
            #pprint(df)
        else:
            pprint(f"{file} is not an EasyLog data file.")

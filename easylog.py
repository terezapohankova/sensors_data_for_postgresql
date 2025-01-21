import pandas as pd
from pprint import pprint
import sys, os

input_folder = r'input_data/easylog_data'
output_folder = r'output_data/easylog'

for subdir, dirs, files in os.walk(input_folder):
    for file in files:
        if file.startswith('ELOG') and file.endswith('.TXT'):
            
            data = pd.read_fwf(os.path.join(input_folder, file))
            df = data.drop(index=[0,1,2,3]).reset_index(drop=True)          

            df['timestamp'] = pd.to_datetime(df['#Name EasyLog034'], format='%d.%m.%Y %H:%M:%S')
            df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df.drop('#Name EasyLog034', axis=1, inplace=True)
            
            df.rename( columns={'Unnamed: 1':'air_temp'}, inplace=True )
            df.rename( columns={'Unnamed: 2':'vbatt'}, inplace=True )
            df.rename( columns={'Unnamed: 3':'in_radiation'}, inplace=True )
            df = df[['timestamp', 'air_temp', 'in_radiation', 'vbatt']]

            df.to_csv(os.path.join(output_folder, r'easylog_postgres.csv'), sep = ',', index=False, mode='a')
            pprint(df)
        else:
            pprint(f"{file} is not an EasyLog data file")



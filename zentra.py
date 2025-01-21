import pandas as pd
from pprint import pprint
import sys, os

input_folder = r'input_data/zentra_data'
output_folder = r'output_data/zentra'

for subdir, dirs, files in os.walk(input_folder):
    for file in files:
        if file.startswith('zentra') and file.endswith('.xlsx'):
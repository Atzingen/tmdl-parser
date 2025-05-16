import os
import json
from data_model import *
from parse_tmdl import TMLDParser

# Load config
config_path = 'config.json'
def get_default_file_path():
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                return config.get('default_file_path', '')
            except Exception:
                return ''
    return ''

# Get file path from config or user input
default_file_path = get_default_file_path()
if default_file_path:
    file_path = default_file_path
else:
    file_path = input("Enter the PBIP file path (or just the filename to use default path): ")
    print("Tip: To avoid this prompt, set 'default_file_path' in config.json.")

# Check if input is just a filename without a path
if os.path.dirname(file_path) == "":
    # Use default path with the given filename
    file_path = os.path.join("pbip", file_path)
# If no input provided, use the default file
if not file_path:
    file_path = 'pbip/PNP_Publicada_dev.pbip'

tmdl = TMLDParser(file_path)
tables = tmdl.parse_all_tables()

for table_name, table_data in tables.items():
    print('\n\n\n')
    print(f"Table Name: {table_name}")
    for t in table_data:
        print(t)

tmdl.save_to_json('output/tables.json')
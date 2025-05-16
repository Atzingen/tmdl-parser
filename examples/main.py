# Example usage of tmdlparser
import os
import json
from tmdlparser import TMLDParser

# Load config
config_path = '../config.json'
def get_default_file_path():
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                return config.get('default_file_path', '')
            except Exception:
                return ''
    return ''

default_file_path = get_default_file_path()
if default_file_path:
    file_path = default_file_path
else:
    file_path = input("Enter the PBIP file path (or just the filename to use default path): ")
    print("Tip: To avoid this prompt, set 'default_file_path' in config.json.")

if os.path.dirname(file_path) == "":
    file_path = os.path.join("../pbip", file_path)
if not file_path:
    raise ValueError("No file path provided. Please set 'default_file_path' in config.json or provide a path when prompted.")

tmdl = TMLDParser(file_path)
tables = tmdl.parse_all_tables()

for table_name, table_data in tables.items():
    print('\n\n\n')
    print(f"Table Name: {table_name}")
    for t in table_data:
        print(t)

tmdl.save_to_json('../output/tables.json')

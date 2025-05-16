import json
import os, sys
from data_model import *

class TMLDParser:
    def __init__(self,
                 pbip_project_path=""):
        self.max_depth = 3
        self.groups = []
        self.tables = {}
        if pbip_project_path:
            self.pbi_project_path = pbip_project_path
        
    def _read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    
    def get_tables(self):
        normalized_path = os.path.normpath(self.pbi_project_path)
        if not os.path.isabs(normalized_path):
            normalized_path = os.path.abspath(normalized_path)
        if not normalized_path.endswith(".pbip"):
            raise ValueError("The provided path (pbi_project_path) does not point to a .pbip file.")
        project_path = os.path.dirname(normalized_path)
        file_name = os.path.basename(normalized_path)
        project_name = os.path.splitext(file_name)[0]
        tables_path = os.path.join(project_path, project_name + '.SemanticModel', 'definition', 'tables')
        tables = os.listdir(tables_path)
        table_paths = [os.path.join(tables_path, table) for table in tables]
        return table_paths

    def _parse_level(self, lines, level=1):
        current_properties = []
        current_element = ''
        current_description = []
        groups = []
        for line in lines:
            if not line.strip():  # remove empty lines
                continue
            if line.startswith('///') and not current_properties and not current_element:  # first description
                current_description.append(line.strip().strip('/// '))
                continue
            elif line.startswith('///'):  #reach a new description
                if level == 2:
                    calc, prop = self._parse_calculation(current_properties)
                else:
                    calc, prop = [], current_properties
                tmdl = TMDL.create(description=current_description, 
                                   element=current_element, 
                                   properties=prop,
                                   calculation=calc)
                groups.append(tmdl)
                current_description = [line.strip().strip('/// ')]
                current_properties = []
                current_element = ''
                continue
            if line[0] == '\t':     # idented content goes to properties
                current_properties.append(line[1:])
            else:
                if current_element:  # reach a new element (store content)
                    if level == 2:
                        calc, prop = self._parse_calculation(current_properties)
                    else:
                        calc, prop = [], current_properties
                    tmdl = TMDL.create(description=current_description, 
                                       element=current_element, 
                                       properties=prop,
                                       calculation=calc)
                    groups.append(tmdl)
                    current_description = []
                    current_properties = []
                current_element = line.strip()
        if level == 2:
            calc, prop = self._parse_calculation(current_properties)
        else:
            calc, prop = [], current_properties
        tmdl = TMDL.create(description=current_description, 
                           element=current_element, 
                           properties=prop,
                           calculation=calc)
        groups.append(tmdl)
        return groups
    
    def _parse_calculation(self, prop_list):
        prop = []
        calc = []
        for p in prop_list:
            if p.startswith('\t'):
                calc.append(p[1:])
            else:
                prop.append(p)
        return calc, prop

    def _parse_tables(self):
        groups = []
        for level in range(1, self.max_depth + 1):
            if level == 1:
                groups = self._parse_level(self.lines)
            if level == 2:
                for i, group in enumerate(groups):
                    group_2 = self._parse_level(group.properties, level=2)
                    groups[i].properties = group_2
        self.groups = groups

    def parse_file(self, file_path):
        self.lines = self._read_file(file_path)
        self._parse_tables()
        return self.groups
    
    def parse_all_tables(self):
        tables = self.get_tables()
        for table in tables:
            table_name = os.path.basename(table)
            result = self.parse_file(table)
            self.tables[table_name] = result
        return self.tables
    
    def _tmdl_to_dict(self, tmdl):
        """
        Recursively converts a TMDL object (and its nested TMDL objects in 'properties') 
        into a dictionary suitable for JSON serialization.
        """
        return {
            "description": tmdl.description,
            "element": tmdl.element,
            "calculation": tmdl.calculation,
            "properties": [
                self._tmdl_to_dict(prop) if isinstance(prop, TMDL) else prop
                for prop in tmdl.properties
            ],
        }

    def save_to_json(self, output_path):
        """
        Saves the parsed TMDL structure into a JSON file at the given output path.
        If tables were not previously parsed, it will parse them before saving.
        """
        if not self.tables:
            self.parse_all_tables()

        data = {}
        for table_name, tmdls in self.tables.items():
            data[table_name] = [self._tmdl_to_dict(t) for t in tmdls]

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {output_path}")

    def __str__(self):
        return "\n\n".join(str(group) for group in self.groups)

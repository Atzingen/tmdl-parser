import json
import os, sys
from .data_model import *

class TMDLParser:
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
                    calc_list, prop = self._parse_calculation(current_properties)
                    calc_str = '\n'.join(calc_list)
                else:
                    calc_str, prop = '', current_properties # Ensure calc_str is a string
                tmdl = TMDL.create(description='\n'.join(current_description),
                                   element=current_element, 
                                   properties=prop,
                                   calculation=calc_str) # Pass the joined string
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
                        calc_list, prop = self._parse_calculation(current_properties)
                        calc_str = '\n'.join(calc_list)
                    else:
                        calc_str, prop = '', current_properties # Ensure calc_str is a string
                    tmdl = TMDL.create(description='\n'.join(current_description),
                                       element=current_element, 
                                       properties=prop,
                                       calculation=calc_str) # Pass the joined string
                    groups.append(tmdl)
                    current_description = []
                    current_properties = []
                current_element = line.strip()
        if level == 2:
            calc_list, prop = self._parse_calculation(current_properties)
            calc_str = '\n'.join(calc_list)
        else:
            calc_str, prop = '', current_properties # Ensure calc_str is a string
        tmdl = TMDL.create(description='\n'.join(current_description),
                           element=current_element, 
                           properties=prop,
                           calculation=calc_str) # Pass the joined string
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
    
    def to_dict(self) -> dict:
        """
        Return the parsed TMDL structure as a nested Python dictionary of the
        form ``{table_name: [tmdl_dict, ...]}``. If tables have not been
        parsed yet, :meth:`parse_all_tables` is called first.
        """
        if not self.tables:
            self.parse_all_tables()
        return {
            table_name: [t.to_dict() for t in tmdls]
            for table_name, tmdls in self.tables.items()
        }

    def to_dataframe(self, flatten: bool = True):
        """
        Return the parsed TMDL structure as a pandas ``DataFrame``.

        Pandas is an optional dependency; install it via
        ``pip install tmdl-parser[pandas]``.

        Parameters
        ----------
        flatten:
            When ``True`` (default) every nested TMDL (typically columns and
            measures inside a table) becomes its own row, with
            ``parent_element`` pointing back to the enclosing table. When
            ``False`` only top-level TMDL entries are emitted and their
            ``properties`` column keeps the raw Python objects.
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install with: pip install tmdl-parser[pandas]"
            ) from exc

        if not self.tables:
            self.parse_all_tables()

        rows = []
        for table_name, tmdls in self.tables.items():
            for tmdl in tmdls:
                if flatten:
                    rows.extend(self._flatten_tmdl(tmdl, table_name))
                else:
                    rows.append({
                        "table": table_name,
                        "parent_element": "",
                        "element": tmdl.element,
                        "description": tmdl.description,
                        "calculation": tmdl.calculation,
                        "properties": tmdl.properties,
                    })
        columns = ["table", "parent_element", "element",
                   "description", "calculation", "properties"]
        return pd.DataFrame(rows, columns=columns)

    def _flatten_tmdl(self, tmdl, table_name, parent_element=""):
        """
        Yield dict rows for ``tmdl`` and any nested TMDL objects inside its
        ``properties`` list. Non-TMDL (raw string) properties stay attached
        to the parent row as a list.
        """
        scalar_props = [p for p in tmdl.properties if not isinstance(p, TMDL)]
        nested = [p for p in tmdl.properties if isinstance(p, TMDL)]

        rows = [{
            "table": table_name,
            "parent_element": parent_element,
            "element": tmdl.element,
            "description": tmdl.description,
            "calculation": tmdl.calculation,
            "properties": scalar_props,
        }]
        for child in nested:
            rows.extend(self._flatten_tmdl(child, table_name, tmdl.element))
        return rows

    def save_to_json(self, output_path):
        """
        Saves the parsed TMDL structure into a JSON file at the given output path.
        If tables were not previously parsed, it will parse them before saving.
        """
        data = self.to_dict()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {output_path}")

    def __str__(self):
        return "\n\n".join(str(group) for group in self.groups)

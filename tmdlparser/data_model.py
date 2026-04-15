from dataclasses import dataclass, field

@dataclass
class TMDL:
    """
    Data structure for TMDL (Table/Measure/Dimension/Line) objects extracted 
    from the Power BI TMDL format, intended for use with Jinja2 templates.
    """
    description: str = ''
    element: str = ""
    properties: list = field(default_factory=lambda: [])
    calculation: str = ''

    @classmethod
    def create(cls, description, element, properties, calculation=''):
        """
        Create a new TMDL object with the specified parameters.
        """
        return cls(description, element, properties, calculation)

    def to_dict(self) -> dict:
        """
        Recursively convert this TMDL object into a plain dictionary.
        Nested TMDL objects inside ``properties`` are converted as well;
        non-TMDL entries (raw strings) are kept as-is.
        """
        return {
            "description": self.description,
            "element": self.element,
            "calculation": self.calculation,
            "properties": [
                prop.to_dict() if isinstance(prop, TMDL) else prop
                for prop in self.properties
            ],
        }

    def __str__(self):
        """
        Return a string representation of the TMDL object.
        """
        prop_str = "\n".join(
            f"\t{'-' * 10}\n\tDescription: {prop.description}\n\tElement: {prop.element}\n\tProps: {prop.properties}\n\tCalcs: {prop.calculation}"
            if isinstance(prop, TMDL) else f"\t{prop}"
            for prop in self.properties
        )
        return (
            f"Description: \n{self.description}\n"
            f"Element: \n{self.element}\n"
            f"Properties:\n{prop_str}\n"
            f"Calculation: {self.calculation}\n{'-' * 20}"
        )


@dataclass
class Table:
    """
    Data structure for a regular table extracted from the Power BI JSON 
    (DataModelSchema), intended for use with Jinja2 templates.
    """
    name: str
    columns: list = field(default_factory=lambda: [])
    description: str = ''
    author: str = ''
    version: str = ''
    date: str = ''


@dataclass
class Column:
    """
    Data structure for a column extracted from the Power BI JSON 
    (DataModelSchema), intended for use with Jinja2 templates.
    """
    name: str
    summarizeBy: str = ''
    dataType: str = ''
    description: str = ''
    author: str = ''
    version: str = ''
    date: str = ''


@dataclass
class Measure:
    """
    Data structure for a measure extracted from the Power BI JSON 
    (DataModelSchema), intended for use with Jinja2 templates.
    """
    name: str
    dax: str = ''
    description: str = ''
    author: str = ''
    version: str = ''
    date: str = ''


@dataclass
class CalculatedColumn:
    """
    Data structure for a calculated column extracted from the Power BI JSON 
    (DataModelSchema), intended for use with Jinja2 templates.
    """
    name: str
    calc_code: str = ''
    summarizeBy: str = ''
    description: str = ''
    author: str = ''
    version: str = ''
    date: str = ''

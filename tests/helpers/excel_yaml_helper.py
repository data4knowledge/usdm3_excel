import os
import pandas as pd
import yaml
from typing import Dict, List, Any


class ExcelYamlHelper:
    """
    Helper class for testing that provides operations to save Excel file content to YAML
    and compare Excel file content with YAML file content.

    The YAML structure is:
    {
        "sheet_name1": [
            [cell1, cell2, ...],  # row 1
            [cell1, cell2, ...],  # row 2
            ...
        ],
        "sheet_name2": [
            ...
        ],
        ...
    }
    """

    def __init__(self, excel_file: str, yaml_file: str):
        """
        Initialize the helper with Excel file and YAML file paths.

        Args:
            excel_file: Path to the Excel file
            yaml_file: Path to the YAML results file
        """
        self.excel_file = excel_file
        self.yaml_file = yaml_file

    def _read_excel(self) -> Dict[str, List[List[Any]]]:
        """
        Read the Excel file and convert it to a dictionary with sheet names as keys
        and lists of rows as values.

        Returns:
            Dictionary with sheet names as keys and lists of rows as values
        """
        # Check if file exists
        if not os.path.exists(self.excel_file):
            raise FileNotFoundError(f"Excel file not found: {self.excel_file}")

        # Read all sheets from the Excel file
        excel_data = pd.read_excel(self.excel_file, sheet_name=None)

        # Convert to the required format
        result = {}
        for sheet_name, df in excel_data.items():
            # Convert DataFrame to list of lists (rows)
            rows = []
            for _, row in df.iterrows():
                # Convert row to list and handle NaN values
                row_list = []
                for value in row:
                    if pd.isna(value):
                        row_list.append(None)
                    else:
                        row_list.append(value)
                rows.append(row_list)
            result[sheet_name] = rows

        return result

    def _read_yaml(self) -> Dict[str, List[List[Any]]]:
        """
        Read the YAML file.

        Returns:
            Dictionary with sheet names as keys and lists of rows as values
        """
        # Check if file exists
        if not os.path.exists(self.yaml_file):
            raise FileNotFoundError(f"YAML file not found: {self.yaml_file}")

        # Read YAML file
        with open(self.yaml_file, "r") as file:
            return yaml.safe_load(file)

    def save(self) -> None:
        """
        Save the Excel file content to the YAML file.

        Returns:
            None
        """
        # Read Excel file
        excel_data = self._read_excel()

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.yaml_file), exist_ok=True)

        # Write to YAML file
        with open(self.yaml_file, "w") as file:
            yaml.dump(excel_data, file, default_flow_style=False)

    def compare(self) -> bool:
        """
        Compare the Excel file with the YAML results file without saving.

        Returns:
            True if the content is the same, False otherwise
        """
        try:
            # Read Excel and YAML files
            excel_data = self._read_excel()
            yaml_data = self._read_yaml()

            # Compare the data
            return excel_data == yaml_data
        except FileNotFoundError:
            # If either file doesn't exist, return False
            return False

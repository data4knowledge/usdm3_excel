from usdm3_excel import USDM3Excel
from tests.helpers.excel_yaml_helper import ExcelYamlHelper

SAVE = True

def test_integration():
    usdm3_excel = USDM3Excel()
    usdm3_excel.to_excel(
        "tests/test_files/usdm.json", "tests/test_files/usdm_excel.xlsx"
    )
    helper = ExcelYamlHelper("tests/test_files/usdm_excel.xlsx", "tests/test_files/usdm_excel.yaml")
    if SAVE:
        helper.save()
    assert helper.compare
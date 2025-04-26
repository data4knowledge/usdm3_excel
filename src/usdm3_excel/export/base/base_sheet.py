from .ct_version import CTVersion
from usdm3_excel.excel_table_writer.excel_table_writer import ExcelTableWriter


class BaseSheet:
    HEADING_BG = "D9D9D9"

    def __init__(self, ct_version: CTVersion, etw: ExcelTableWriter):
        self.ct_version = ct_version
        self.etw = etw

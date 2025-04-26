from src.usdm4_excel import USDM4Excel

filepath = "/Users/daveih/Documents/python/sdw_test/USDM4/d051771e-4b5c-48a7-9d37-e7e58b40f177/usdm.json"

ue = USDM4Excel()
ue.to_excel(filepath, "excel.xlsx")

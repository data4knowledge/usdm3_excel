from src.usdm3_excel import USDM3Excel

filepath = "/Users/daveih/Documents/python/sdw_test/USDM4/d051771e-4b5c-48a7-9d37-e7e58b40f177/usdm.json"

ue = USDM3Excel()
ue.to_excel(filepath, "excel_1.xlsx")

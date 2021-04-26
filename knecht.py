import json
from tools import table

myTable = table()

#myTable.table_row_load_by_id(1)
# myTable.set_one_col("continent", "europe")
# myTable.set_one_col("year", 2019)
# myTable.table_row_save()

# myTable.set_one_col("name", "Polenca")
# myTable.set_one_col("country", "Spain")
# myTable.table_row_save()

#myTable.table_row_delete_by_id(2)

# myDict = {
#   "name": "Berchtesgaden",
#   #"country": "Bayern",
#   "continent": "Bayern",
#   "planet": "Bayern"
# }
# try:
#   myTable.set_multiple_col(myDict)
# except Exception as e:
#   inf = e

myTable.table_row_load_by_id(2)
myTable.set_one_col("name", "Capx Verde")
myTable.set_one_col("country", "Portugal")
myTable.table_row_save()

#print(json.dumps(myTable.curRow, indent=2))
print(json.dumps(myTable.tableData, indent=2))
#----------------------------------------------------------------
import os
import sys
import json
import copy

#-App Globals----------------------------------------------------



#----------------------------------------------------------------
class table:
  #--class globals---------------------
  curPath = os.path.dirname(os.path.abspath(__file__))
  dataFileName = 'destinations.json'
  dataFilePath = os.path.join(curPath, dataFileName) 

  dataModel = [
    {
      "col": "name",
      "description": "Name of the Destination",
      "type": str,
      "required": True
    },
    {
      "col": "continent",
      "description": "Continent",
      "type": str,
      "required": False
    },
    {
      "col": "country",
      "description": "Country",
      "type": str,
      "required": True
    },
    {
      "col": "language",
      "description": "Language",
      "type": str,
      "required": False
    },
    {
      "col": "hint",
      "description": "Hint",
      "type": str,
      "required": False
    },
    {
      "col": "year",
      "description": "Visited in Year",
      "type": int,
      "required": False
    }
  ]

  #------------------------------------
  def __init__(self):
    
    self.tableData = []
    self.curRow = {}

    self.data_file_check()
    self.data_file_load()

  #------------------------------------
  def data_file_check(self):
    chk = False
    if not os.path.isfile(self.dataFilePath):
      chk = True
    if not chk:
      try:
        flObj = open(self.dataFileName, "r", encoding='utf8')
        json.loads(flObj.read())
        flObj.close()
      except:
        chk = True
      
    if chk:
      flObj = open(self.dataFileName, "w", encoding='utf8')
      flObj.write("[]")
      flObj.close()
  
  #------------------------------------
  def data_file_load(self):
    flObj = open(self.dataFileName, "r", encoding='utf8')
    dataObj = json.loads(flObj.read())
    self.tableData = dataObj
    flObj.close()

  #------------------------------------
  def data_file_save(self):
    flObj = open(self.dataFileName, "w", encoding='utf8')
    jsonStr = json.dumps(self.tableData, indent=2)
    flObj.write(jsonStr)
    flObj.close()

  #------------------------------------
  def create_new_id(self):
    if len(self.tableData ) == 0:
      return 1
    
    idAry = []
    for row in self.tableData:
      idAry.append(row["id"])
    
    maxId = max(idAry)
    newId = maxId + 1
    return newId

  #------------------------------------
  def get_all_ids(self):
    idAry = []
    for row in self.tableData:
      idAry.append(row["id"])
    idAry.sort()

    return idAry

  #------------------------------------
  def table_row_load_by_id(self, id):
    chk = False
    for row in self.tableData:
      if row["id"] == id:
        self.curRow = copy.copy(row) # Das mit dem copy() ist EVIL!!!
        chk = True
        break

    if not chk:
      raise Exception("id '%s' not found in data file" %id)

  #------------------------------------
  def table_row_save(self):
    missingVals = []
    for defi in self.dataModel:
      if defi["required"] and defi["col"] not in self.curRow:
        missingVals.append(defi["col"])

    if len(missingVals) > 0:
      raise Exception("Following values are missing: '%s'" % ', '.join(missingVals) )

    if "id" not in self.curRow:
      self.curRow["id"] = self.create_new_id()
      self.tableData.append(self.curRow)
    else:
      chk = False
      i = 0
      for row in self.tableData:
        if row["id"] == self.curRow["id"]:
          self.tableData[i] = copy.copy(self.curRow)
          chk = True
          break
        i+=1
      
      if not chk:
        raise Exception("Failed to save table current table row: '%s'" %self.curRow )

    self.data_file_save()
    #self.data_file_load()

  #------------------------------------
  def set_one_col(self, key, val):
    colChk = False
    defiIdx = None
    i = 0
    for defi in self.dataModel:
      if key == defi["col"]:
        defiIdx = i 
        colChk = True
      i += 1

    if not colChk:
      raise Exception("Invalid column name / key: '%s'" %key)
    
    if type(val) != self.dataModel[defiIdx]["type"]:
      raise Exception("Invalid value format for: '%s'" %key)
    
    self.curRow[key] = val

  #------------------------------------
  def set_multiple_col(self, dic):
    for key, val in dic.items():
      self.set_one_col(key, val)
  
  #------------------------------------
  def table_row_delete_by_id(self, id):
    chk = False
    idx = None
    i = 0
    for row in self.tableData:
      if row["id"] == int(id):
        idx = i
        chk = True
      i += 1
   
    if not chk:
      raise Exception("id '%s' not found in data file" %id)
    
    tmpDataAry = copy.copy(self.tableData)
    del tmpDataAry[idx]
    self.tableData = tmpDataAry
    self.data_file_save()

  #------------------------------------


  #------------------------------------



#----------------------------------------------------------------

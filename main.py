#-Module Imports---------------------------------------------------
import os, sys
import json 

from flask import Flask, request, session, redirect, jsonify 
from flask_cors import CORS 

from tools import destinations, containers

#-Build the API App------------------------------------------------
#app = Flask(__name__, static_url_path='', static_folder='./webui' )
app = Flask(__name__ )
app.secret_key = "changeit"
app.debug = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


#-Serve the frontend-----------------------------------------------
@app.route('/', methods=["GET"])
def app_home():
  return app.send_static_file("index.html")


#-The API Section--------------------------------------------------
@app.route('/api/json/v1', methods=["GET"])
@app.route('/api', methods=["GET"])
def api_home_get():

  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "message": ""
  }

  name = request.args.get('name')
  if name:
    resObj["name"] = name

  #---------------------
  return jsonify(resObj)

#---------------------------------------------
@app.route('/api/destinations', methods=["GET"])
def api_destinations_get():
  
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "message": ""
  }
  
  myDest = destinations()
  resObj["data"] = myDest.tableData

  # try:
  #   resObj["data"] = myDest.tableDatax
  # except Exception as e:
  #   resObj["status"] = 500
  #   resObj["message"] = "Something went wrong"
  #   return jsonify(resObj), 500

  #---------------------
  return jsonify(resObj)

#---------------------------------------------
@app.route('/api/destinations', methods=["POST"])
def api_destinations_post():
  
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "message": ""
  }

  postIn = request.json

  # requiredKeys = ["name", "country"]
  # missingKeys = []
  # for key in requiredKeys:
  #   if key not in postIn:
  #     missingKeys.append(key)
    
  # if len(missingKeys) > 0:
  #   resObj["status"] = 400
  #   resObj["message"] = "Values missing: %s" %missingKeys
  #   return jsonify(resObj), 400

  myDest = destinations()
  for key, val in postIn.items():
    myDest.set_one_col(key, val)
    
  try:
    myDest.table_row_save()
  except Exception as e:
    resObj["status"] = 400
    resObj["message"] = str(e)
    return jsonify(resObj), 400

  #---------------------
  return jsonify(resObj)

#---------------------------------------------
@app.route('/api/destinations/<id>', methods=["PUT"])
def api_destinations_put(id):
  
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "message": ""
  }

  putIn = request.json
  myDest = destinations(int(id))
  try:
    myDest.set_multiple_col(putIn)
  except Exception as e:
    resObj["status"] = 400
    resObj["message"] = str(e)
    return jsonify(resObj), 400

  myDest.table_row_save()

  #--------------------- 
  return jsonify(resObj)

#---------------------------------------------
@app.route('/api/destinations/<id>', methods=["DELETE"])
def api_destinations_delete(id):
  
  resObj = {
    "path": request.path,
    "method": request.method,
    "status": 200,
    "message": ""
  }

  myDest = destinations()

  try:
    myDest.table_row_delete_by_id(int(id))
  except Exception as e:
    resObj["status"] = 400
    resObj["message"] = str(e)
    return jsonify(resObj), 400
  
  #--------------------- 
  return jsonify(resObj)

#-App Runner-------------------------------------------------------
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
  
#------------------------------------------------------------------
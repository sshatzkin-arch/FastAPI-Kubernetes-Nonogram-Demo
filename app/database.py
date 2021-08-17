import pyodbc 
import os
import sys
from dotenv import load_dotenv
import pathlib
import logging

load_dotenv()
driver = '{/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1}' # For deployment
server = "mssql-deployment.database.svc.cluster.local" # Cluster IP Address for Deployment 
database = 'NonogramDB'
uid = "sa"
password = "<PASSWORD NOT SET>"


#os.getenv("mssql_password") # For Deployment with Kubernetes Secret

# For Local Testing
if (sys.platform == "win32"):
  driver = '{SQL Server}'
  server = '20.75.102.247' # External IP for local testing
  password =  os.environ.get("sa_pass") # For Local Testing

# Get Password from Azure Secrets volume
passfile = pathlib.Path("./mnt/secrets-store/DBPassword")
if passfile.exists ():
  passFile = open("./mnt/secrets-store/DBPassword", "r")
  password = passFile.readline()
  print("Password Found and Loaded")
else:
  print("Password Secret File Not Found")
  

def connect ():
  conn = None
  if password != None:
    connect_str = 'Driver='+ driver + ';' + 'Server=' + server + ';' + 'Database=' + database + ';' + 'uid=' + uid + ';' +'PWD=' + str(password) + ';'
    print(connect_str) #-> Security issue bc it prints password to logs
    conn = pyodbc.connect(connect_str)
  else:
    print("NO PASSWORD VALUE")
  return conn


def get_nonos(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Nonograms')
  return cursor_to_dict(cursor)

def get_nonos_by(conn, ID = None, name = None, min_width = 0, min_height = 0, max_width = 10000, max_height = 10000):
  cursor = conn.cursor()
  id_str = ""
  if (ID != None):
    id_str = f"ID={str(ID)} AND "
  
  name_str = ""
  if (name != None):
    name_str = f"name=\'{name}\' AND "
  
  width_str =  f"width>{min_width} AND width<{max_width}"
  height_str =  f"height>{min_height} AND height<{max_height}"
  sql = f"SELECT * FROM Nonograms WHERE {id_str}{name_str}{width_str} AND {height_str}"
  print(sql)
  cursor.execute(sql)
  return cursor_to_dict(cursor), sql

def push_nono(conn, puzz):
  cursor = conn.cursor()
  sql = f"INSERT INTO Nonograms VALUES (\'{puzz['name']}\', {str(puzz['width'])}, {str(puzz['height'])}, \'{puzz['solution']}\', \'{puzz['col_hints']}\', \'{puzz['row_hints']}\')"
  #(Name, Width, Height, Solution, Col_hints, Row_hints)
  print(sql)
  cursor.execute(sql)
  print("Pushed: " + str(puzz))
  conn.commit()

def print_nonos(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Nonograms')

  for row in cursor:
      print(row)

def cursor_to_dict (cursor):
  columns = [column[0] for column in cursor.description]
  results = []
  for row in cursor.fetchall():
    results.append(dict(zip(columns, row)))

  return results
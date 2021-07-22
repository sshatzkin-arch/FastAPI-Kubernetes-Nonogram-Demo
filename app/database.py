import pyodbc 
import os
import sys
from dotenv import load_dotenv

load_dotenv()
driver = '{/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1}' # For deployment
server = "mssql-deployment.database.svc.cluster.local" # Cluster IP Address for Deployment 
database = 'NonogramDB'
uid = "sa"
password = os.getenv("mssql_password") # For Deployment

# For Local Testing
if (sys.platform == "win32"):
  driver = '{SQL Server}'
  server = '127.0.0.1,1433' # External IP for local testing
  password =  os.environ.get("sa_pass") # For Local Testing


def connect ():
  connect_str = 'Driver='+ driver + ';' + 'Server=' + server + ';' + 'Database=' + database + ';' + 'uid=' + uid + ';' +'PWD=' + password + ';'
  print(connect_str)
  conn = pyodbc.connect(connect_str)
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
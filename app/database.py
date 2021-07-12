import pyodbc 
import os

#driver = '{/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1}' # For deployment
driver = '{SQL Server}' # For local testing

#server = '10.107.6.107' # Cluster IP Address for Deployment 
server = '127.0.0.1,63656' # External IP for local testing

database = 'NonogramDB'
uid = "sa"

#password = os.getenv("mssql_password") # For Deployment
password = 'yourStrong(!)Password' # For Local Testing

def connect ():
  conn = pyodbc.connect('Driver='+ driver + ';' + 'Server=' + server + ';' + 'Database=' + database + ';' + 'uid=' + uid + ';' +'PWD=' + password + ';') #+ 'Trusted_Connection=yes;')

  return conn


def get_nonos(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Nonograms')
  return cursor_to_dict(cursor)

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
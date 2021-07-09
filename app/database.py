import pyodbc 
import os

driver = '{/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1}'
#driver = '{SQL Server}' # For local testing
server = '10.107.6.107' # Cluster IP Address
#server = '127.0.0.1,64596' # External IP for local testing
#server = os.getenv("mssql_server_address")

database = 'NonogramDB'
uid = "sa"

#password = os.getenv("mssql_password")
password = 'yourStrong(!)Password'

def connect ():
  conn = pyodbc.connect('Driver='+ driver + ';' + 'Server=' + server + ';' + 'Database=' + database + ';' + 'uid=' + uid + ';' +'PWD=' + password + ';') #+ 'Trusted_Connection=yes;')

  return conn


def get_nonos(conn):
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM Nonograms')


  return cursor_to_dict(cursor)

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
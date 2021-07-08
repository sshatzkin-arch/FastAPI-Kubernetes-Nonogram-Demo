import pyodbc 

server = '127.0.0.1,64596'
database = 'NonogramDB'
uid = "sa"
password = 'yourStrong(!)Password'


def connect ():
  conn = pyodbc.connect('Driver={SQL Server};' + 'Server=' + server + ';' + 'Database=' + database + ';' + 'uid=' + uid + ';' +'PWD=' + password + ';') #+ 'Trusted_Connection=yes;')

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
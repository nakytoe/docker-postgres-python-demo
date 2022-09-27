import psycopg2
import yaml
import sys

###
### a script that establishes a connection to given postgres database
###

args = sys.argv

# get secrets as arguments in following order:
DATABASE = args[1]
USER = args[2]
PASSWORD = args[3]
HOST = args[4]
PORT = args[5]

# below inspired by: https://www.tutorialspoint.com/python_data_access/python_postgresql_database_connection.htm

# establish connection
conn = psycopg2.connect(
   database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
)
# create cursor
cursor = conn.cursor()

# execute an MYSQL function using the execute() method
cursor.execute("select version()")

# fetch a single row
data = cursor.fetchone()
print("Connection established to: ",data)

# close connection
conn.close()

exit()
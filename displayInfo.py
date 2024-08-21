import mysql.connector
from db_config import mysql_config

# Connect to the database
db = mysql.connector.connect(**mysql_config)
cursor = db.cursor(dictionary=True)

# Execute a SELECT query
cursor.execute("SELECT * FROM students")

# Fetch all rows
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
db.close()
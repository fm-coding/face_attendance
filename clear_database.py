import mysql.connector
from db_config import mysql_config

def clear_database():
    try:
        # Initialize MySQL connection
        db = mysql.connector.connect(**mysql_config)
        cursor = db.cursor()

        # Clear the students table
        cursor.execute("TRUNCATE TABLE students")
        db.commit()

        print("Database cleared successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    clear_database()
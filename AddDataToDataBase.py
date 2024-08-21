import cv2
import os
import mysql.connector
from db_config import mysql_config
from datetime import datetime, timedelta

# Initialize MySQL connection
db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()

def create_table_if_not_exists():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(50),
        major VARCHAR(50),
        starting_year INT,
        total_attendance INT,
        standing VARCHAR(5),
        year INT,
        last_attendance_time DATETIME
    )
    """)
    db.commit()

def add_student_to_db(id, name, major, starting_year, total_attendance, standing, year, last_attendance_time):
    sql = """INSERT INTO students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
             ON DUPLICATE KEY UPDATE
             name = VALUES(name),
             major = VALUES(major),
             starting_year = VALUES(starting_year),
             total_attendance = VALUES(total_attendance),
             standing = VALUES(standing),
             year = VALUES(year),
             last_attendance_time = VALUES(last_attendance_time)"""
    values = (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time)
    cursor.execute(sql, values)
    db.commit()
    print(f"Student {name} with ID {id} has been added/updated in the database.")

def resize_and_save_image(id):
    image_path = f'Images/{id}.png'
    if not os.path.exists(image_path):
        print(f"Error: Image file for ID {id} not found in the Images folder.")
        return False
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to read image at {image_path}")
        return False
    
    resized_img = cv2.resize(img, (216, 216))
    cv2.imwrite(image_path, resized_img)
    print(f"Image resized and saved to {image_path}")
    return True

def get_user_input():
    id = input("Enter student ID: ")
    if not resize_and_save_image(id):
        print("Failed to process the image. Student will not be added.")
        return None
    
    name = input("Enter student name: ")
    major = input("Enter student major: ")
    starting_year = input("Enter starting year: ")
    total_attendance = int(input("Enter total attendance: "))
    standing = input("Enter standing (e.g., G for Good): ")
    year = int(input("Enter current year: "))
    last_attendance_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    return id, name, major, starting_year, total_attendance, standing, year, last_attendance_time

def main():
    create_table_if_not_exists()
    while True:
        print("\nAdding a new student to the database:")
        student_data = get_user_input()
        if student_data:
            add_student_to_db(*student_data)
        
        continue_adding = input("\nDo you want to add another student? (y/n): ").lower()
        if continue_adding != 'y':
            break

    print("All students have been added to the database.")

if __name__ == "__main__":
    main()

# Close MySQL connection when done
db.close()
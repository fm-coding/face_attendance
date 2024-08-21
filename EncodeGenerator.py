import cv2
import face_recognition
import pickle
import os
import mysql.connector
from db_config import mysql_config

# Initialize MySQL connection
db = mysql.connector.connect(**mysql_config)
cursor = db.cursor()

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    if img is not None:
        imgList.append(img)
        studentIds.append(os.path.splitext(path)[0])
    else:
        print(f"Warning: Unable to read image {path}")

def findEncodings(imagesList):
    encodeList = []
    for i, img in enumerate(imagesList):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print(f"Warning: No face found in image for student ID {studentIds[i]}")
        except Exception as e:
            print(f"Error processing image for student ID {studentIds[i]}: {str(e)}")
    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Print summary
print(f"Total images processed: {len(imgList)}")
print(f"Successful encodings: {len(encodeListKnown)}")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

# Close MySQL connection when done
db.close()
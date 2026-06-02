import csv
import cv2
import os
from datetime import datetime

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

dataset_path = "dataset"

label_map = {}
current_id = 0

for user in sorted(os.listdir(dataset_path)):

    user_path = os.path.join(dataset_path, user)

    if os.path.isdir(user_path):

        label_map[current_id] = user
        current_id += 1

cam = cv2.VideoCapture(0)

print("Face recognition started")

authenticated = False
name = "UNKNOWN"
decision_made = False

while True:

    ret, frame = cam.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.2, 5)

    if len(faces) > 0 and not decision_made:

        (x, y, w, h) = faces[0]

        face_img = gray[y:y+h, x:x+w]

        id, confidence = recognizer.predict(face_img)

        if confidence < 50:

            name = label_map.get(id, "UNKNOWN")
            text = f"ACCESS GRANTED: {name}"
            authenticated = True

        else:

            text = "ACCESS DENIED"

        decision_made = True

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.imshow("Face Recognition", frame)

        cv2.waitKey(3000)

        break

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) == 27:
        break

time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("Logs.txt", "a") as log:

    if authenticated:

        log.write(f"{time_now} | {name} | ACCESS GRANTED\n")

        print(f"{time_now} | {name} | ACCESS GRANTED")

    else:

        log.write(f"{time_now} | UNKNOWN | ACCESS DENIED\n")

        print(f"{time_now} | UNKNOWN | ACCESS DENIED")

if not authenticated:

    cv2.imwrite("intruder.jpg", frame)

today = datetime.now().strftime("%Y-%m-%d")

current_time = datetime.now().strftime("%H:%M:%S")

hour_min = datetime.now().strftime("%H:%M")

attendance_file = "attendance.csv"

records = []

if os.path.exists(attendance_file):

    with open(attendance_file, "r") as file:

        reader = csv.reader(file)

        records = list(reader)

user_found = False

for row in records:

    if len(row) >= 5:

        recorded_name = row[0]

        recorded_date = row[1]

        if recorded_name == name and recorded_date == today:

            user_found = True

            if row[3] == "-":

                row[3] = current_time

                if hour_min < "16:30":

                    row[4] = "Half Day"

                else:

                    row[4] = "Present"

            break

if not user_found and authenticated:

    status = "Present"

    if hour_min > "09:00" and hour_min < "16:30":

        status = "Half Day"

    records.append([
        name,
        today,
        current_time,
        "-",
        status
    ])

with open(attendance_file, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerows(records)

cam.release()

cv2.destroyAllWindows()
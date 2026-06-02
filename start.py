import cv2
import os
import numpy as np
import sys

user_id = sys.argv[1]

dataset_path = "dataset"
user_folder = os.path.join(dataset_path, user_id)
if not os.path.exists(user_folder):
    os.makedirs(user_folder)
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

count = 0

print("Registration started. Please look at the camera...")

while True:

    ret, frame = cam.read()

    if not ret:
        print("Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        count += 1

        face_img = gray[y:y+h, x:x+w]

        file_path = f"{user_folder}/face_{count}.jpg"

        cv2.imwrite(file_path, face_img)

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        cv2.waitKey(100)

    cv2.imshow("Register Face", frame)

   
    if count >= 15:
        break


    if cv2.waitKey(1) == 27:
        break


cam.release()
cv2.destroyAllWindows()
print("Registration complete for:", user_id)
faces = []
ids = []
label_map = {}

current_id = 0

for user in os.listdir(dataset_path):

    user_path = os.path.join(dataset_path, user)

    if os.path.isdir(user_path):

        label_map[current_id] = user

        for image_name in os.listdir(user_path):

            img_path = os.path.join(user_path, image_name)

            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            if img is not None:
                faces.append(img)
                ids.append(current_id)

        current_id += 1


ids = np.array(ids)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, ids)
recognizer.save("face_model.yml")

print("Model training complete.")
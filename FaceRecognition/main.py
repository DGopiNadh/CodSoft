import os
import cv2
import numpy as np

haar_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haar_cascade_path)

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return faces

def prepare_training_data(data_folder_path):
    faces = []
    labels = []
    label_map = {}
    current_label = 0

    for person_name in sorted(os.listdir(data_folder_path)):
        person_path = os.path.join(data_folder_path, person_name)
        if not os.path.isdir(person_path):
            continue

        label_map[current_label] = person_name
        print(f"Processing person: {person_name}")

        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path, image_name)
            print(f"  Reading image: {image_path}")
            image = cv2.imread(image_path)
            if image is None:
                print(f"    Warning: Unable to load {image_path}")
                continue

            detected_faces = detect_faces(image)
            if len(detected_faces) == 0:
                print(f"    No face detected in {image_path}")
                continue

            (x, y, w, h) = detected_faces[0]
            face = image[y:y+h, x:x+w]
            face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face_resized = cv2.resize(face_gray, (200, 200))

            faces.append(face_resized)
            labels.append(current_label)
            print(f"    Face detected and added for label {person_name}")

        current_label += 1

    return faces, labels, label_map


def train_recognizer(faces, labels):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    return recognizer

def recognize_faces_in_image(image_path, recognizer, label_map):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Cannot load image {image_path}")
        return

    detected_faces = detect_faces(image)
    if len(detected_faces) == 0:
        print("No faces detected in the test image.")
        return

    for (x, y, w, h) in detected_faces:
        face = image[y:y+h, x:x+w]
        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face_resized = cv2.resize(face_gray, (200, 200))

        label, confidence = recognizer.predict(face_resized)
        person_name = label_map.get(label, "Unknown")

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"{person_name} ({int(confidence)})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        print(f"Detected {person_name} with confidence {confidence}")

    cv2.imshow("Face Recognition", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Preparing training data...")
    faces, labels, label_map = prepare_training_data("faces")
    print(f"Total faces collected: {len(faces)}")
    print(f"Label map: {label_map}")

    if len(faces) == 0:
        print("No faces found for training. Exiting.")
        exit(1)

    print("Training recognizer...")
    recognizer = train_recognizer(faces, labels)

    print("Recognizing faces in test image...")
    recognize_faces_in_image("faces/test.jpg", recognizer, label_map)

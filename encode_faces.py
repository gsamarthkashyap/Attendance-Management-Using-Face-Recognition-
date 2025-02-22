import os
import cv2
import face_recognition
import pickle

# Path to dataset folder
dataset_path = "dataset"
encoding_file = "encodings.pickle"

# Load existing encodings if file exists
if os.path.exists(encoding_file):
    with open(encoding_file, "rb") as f:
        known_face_encodings, known_face_names = pickle.load(f)
    print(f"✅ Loaded existing encodings: {len(known_face_names)} faces.")
else:
    known_face_encodings = []
    known_face_names = []
    print("⚠️ No existing encodings found. Creating a new encoding file.")

# Encode faces from dataset folder
for file_name in os.listdir(dataset_path):
    file_path = os.path.join(dataset_path, file_name)

    # Ensure it's an image file
    if not file_name.lower().endswith((".jpg", ".png", ".jpeg")):
        continue

    # Extract name (remove file extension)
    name = os.path.splitext(file_name)[0]

    # Skip encoding if name already exists
    if name in known_face_names:
        print(f"⏩ {name} already encoded, skipping...")
        continue

    # Load image and detect face
    image = cv2.imread(file_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)

    if face_encodings:
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(name)
        print(f"✅ Encoded: {name}")
    else:
        print(f"⚠️ No face detected in {file_name}, skipping...")

# Save updated encodings
with open(encoding_file, "wb") as f:
    pickle.dump((known_face_encodings, known_face_names), f)

print(f"✅ Updated encodings: {len(known_face_names)} faces saved.")

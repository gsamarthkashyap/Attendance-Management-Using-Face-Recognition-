import cv2
import face_recognition
import pickle
import pandas as pd
import os
from datetime import datetime

# Load encodings
with open("encodings.pickle", "rb") as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Define Excel file
excel_file = "attendance.xlsx"

# Track last recorded name to prevent duplicate consecutive entries
last_recorded_name = None  

# Initialize DataFrame for the current session
attendance_df = pd.DataFrame(columns=["Name", "Timestamp", "Status"])

while True:
    ret, frame = video_capture.read()
    if not ret:
        break  # Exit loop if the frame is not captured properly

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces and encodings
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Record attendance only if it's a new detection
        if name != last_recorded_name:
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
            status = "Present" if name != "Unknown" else "NA"

            # Append new entry to DataFrame
            new_entry = pd.DataFrame([{"Name": name, "Timestamp": timestamp, "Status": status}])
            attendance_df = pd.concat([attendance_df, new_entry], ignore_index=True)

            last_recorded_name = name  # Update last recorded name

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Green box

        # Display name below the face
        cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show webcam feed
    cv2.imshow("Face Recognition", frame)

    # Exit if 'q' is pressed or window is closed
    if cv2.waitKey(1) & 0xFF == ord("q") or cv2.getWindowProperty("Face Recognition", cv2.WND_PROP_VISIBLE) < 1:
        break

# ✅ Save attendance to a new sheet in the Excel file
sheet_name = datetime.now().strftime("%d-%m-%Y_%H-%M")
if os.path.exists(excel_file):
    with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="new") as writer:
        attendance_df.to_excel(writer, sheet_name=sheet_name, index=False)
else:
    with pd.ExcelWriter(excel_file, mode="w", engine="openpyxl") as writer:
        attendance_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Attendance saved to sheet: {sheet_name}")

# Cleanup
video_capture.release()
cv2.destroyAllWindows()

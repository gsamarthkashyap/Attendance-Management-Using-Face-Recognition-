import cv2
import face_recognition
import os
import time

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Create dataset folder if it doesn't exist
os.makedirs("dataset", exist_ok=True)

print("Press 's' to save the detected face, 'q' to quit.")

label = None  # Store label name once to avoid blocking input

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(frame)

    # Draw rectangles around detected faces
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the webcam feed
    cv2.imshow("Live Webcam Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and face_locations:
        if label is None:
            label = input("Enter label for this face (or type 'q' to quit): ").strip()
            if label.lower() == 'q':
                break

        top, right, bottom, left = face_locations[0]
        face_image = frame[top:bottom, left:right]  # Crop face

        timestamp = int(time.time())  # Unique identifier
        image_path = f"dataset/{label}_{timestamp}.jpg"
        cv2.imwrite(image_path, face_image)
        print(f"Saved face as {image_path}")

    elif key == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()

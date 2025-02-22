import cv2
import face_recognition
import pickle
import pandas as pd
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Load face encodings
with open("encodings.pickle", "rb") as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Global variables
video_capture = None
running = False
attendance_data = []
excel_file = "attendance.xlsx"

# Initialize Tkinter
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("800x600")
root.configure(bg="#2E4053")

# Header
header_label = tk.Label(root, text="Face Recognition Attendance System", font=("Arial", 16, "bold"), bg="#1C2833", fg="white", pady=10)
header_label.pack(fill=tk.X)

# Canvas for video feed
canvas = tk.Label(root, bg="black")
canvas.pack(pady=10)

def start_recognition():
    global video_capture, running
    if running:
        return  # Avoid multiple threads
    running = True
    threading.Thread(target=process_frame, daemon=True).start()

def process_frame():
    global video_capture, running, attendance_data
    video_capture = cv2.VideoCapture(0)
    
    while running:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
            attendance_data.append({"Name": name, "Timestamp": timestamp, "Status": "Present" if name != "Unknown" else "NA"})
            
            # Draw rectangle and name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
        # Convert frame for Tkinter display
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.imgtk = imgtk
        canvas.configure(image=imgtk)
        root.update_idletasks()
    
    video_capture.release()

def stop_recognition():
    global running
    running = False

def save_attendance():
    if not attendance_data:
        messagebox.showwarning("Warning", "No attendance data to save!")
        return
    
    try:
        with pd.ExcelWriter(excel_file, mode="a", engine="openpyxl", if_sheet_exists="new") as writer:
            df = pd.DataFrame(attendance_data)
            df.to_excel(writer, sheet_name=f"Sheet_{datetime.now().strftime('%H%M%S')}", index=False)
        messagebox.showinfo("Success", "Attendance saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save attendance: {e}")
    
    attendance_data.clear()

def close_app():
    stop_recognition()
    root.destroy()

# Buttons
btn_frame = tk.Frame(root, bg="#2E4053")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Start Recognition", command=start_recognition, font=("Arial", 12), bg="#28B463", fg="white", padx=10, pady=5).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Stop Recognition", command=stop_recognition, font=("Arial", 12), bg="#E74C3C", fg="white", padx=10, pady=5).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Save Attendance", command=save_attendance, font=("Arial", 12), bg="#3498DB", fg="white", padx=10, pady=5).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Exit", command=close_app, font=("Arial", 12), bg="#D35400", fg="white", padx=10, pady=5).grid(row=0, column=3, padx=10)

# Run Tkinter main loop
root.mainloop()

This is a **Face Recognition Attendance System** that captures faces, encodes them, and recognizes them to mark attendance. It uses OpenCV and face-recognition libraries for efficient face detection and recognition.  

## 📌 Features  
- **Face Detection & Recognition** – Detects and recognizes faces in real-time using a webcam.  
- **Face Encoding** – Stores face encodings for future recognition.  
- **Attendance Marking** – Recognizes stored faces and logs attendance.  

## 🛠 Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
```

### 2️⃣ Install Dependencies  
Ensure you have Python installed, then run:  
```bash
pip install -r requirements.txt
```

### 3️⃣ Prepare the Dataset  
- Store images of known individuals in the `dataset/` folder.  
- Run the encoding script to process and save facial encodings.  

## 🚀 Usage  

### Capturing Faces  
```bash
python capture_faces.py
```
Captures images and stores them in the dataset folder.  

### Encoding Faces  
```bash
python encode_faces.py
```
Encodes stored images for recognition.  

### Running Attendance System  
```bash
python face_recognition_attendance.py
```
Detects faces and marks attendance for recognized individuals.  

## 📂 Project Structure  
```
face_recognition/
│── dataset/                     # Folder for storing face images  
│── encodings.pickle              # Serialized face encodings  
│── capture_faces.py              # Script to capture face images  
│── encode_faces.py               # Script to encode face images  
│── face_recognition_attendance.py # Main attendance recognition script  
│── README.md                     # Project documentation  
│── requirements.txt               # Python dependencies  
```

## 🛠 Dependencies  
- **OpenCV** – Video processing & face detection  
- **face-recognition** – Face encoding & recognition  
- **NumPy** – Numerical operations  

Install all dependencies using:  
```bash
pip install -r requirements.txt
```

## 📜 License  
This project is open-source. You are free to use and modify it.  

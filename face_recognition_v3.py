import face_recognition
import cv2
import os
import numpy as np

def load_known_faces(folder_path="proyect\known_faces"):
    """Load and encode known faces"""
    print("Loading known faces...")
    
    known_face_encodings = []
    known_face_names = []
    
    if not os.path.exists(folder_path):
        print(f"Creating {folder_path} directory...")
        os.makedirs(folder_path)
        print("Please add face images to the 'known_faces' folder and run again.")
        return [], []
    
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            name = filename.split('.')[0]
            image_path = os.path.join(folder_path, filename)
            
            print(f"Loading {filename}...")
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(name)
                print(f"Successfully encoded {name}")
            else:
                print(f"No face found in {filename}")
    
    return known_face_encodings, known_face_names

def start_camera(known_face_encodings, known_face_names):
    """Start face recognition with webcam"""
    print("Starting camera...")
    
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Camera started successfully. Press 'q' to quit.")
    
    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert the image from BGR color to RGB color
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find all face locations in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        # Find all face encodings in the current frame
        if face_locations:  # Only process if faces are found
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            # Loop through each face in this frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name = "INTRUDER"
                
                # Scale back up face locations since we scaled down the image
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # See if the face is a match for the known faces
                if known_face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    if True in matches:
                        name = known_face_names[matches.index(True)]
                
                # Draw box and label
                color = (0, 255, 0) if name != "INTRUDER" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
        
        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

def main():
    known_face_encodings, known_face_names = load_known_faces()
    
    if not known_face_encodings:
        print("No faces loaded. Please add images to the 'known_faces' folder.")
        return
    
    start_camera(known_face_encodings, known_face_names)

if __name__ == "__main__":
    main()
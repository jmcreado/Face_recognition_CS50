# Face Recognition Application

#### Video Demo:  <URL HERE>

#### Description:

**Project Overview**  
This project is a Flask-based application designed to identify faces using a camera and recognize them based on pre-uploaded tagged photos. The app also alerts if an unrecognized face ("intruder") is detected. Users can upload multiple photos to create a face database, and the system uses this database for real-time face recognition. The recognition module is built using `face_recognition` and OpenCV libraries to ensure high accuracy and performance.

During the initial stages of the project, I explored using YOLO (You Only Look Once) for face recognition. However, due to the high volume of images required for effective training and the associated computational costs, YOLO proved to be inefficient for this specific application. As a result, I transitioned to using the `face_recognition` library, which offered a more accessible and efficient solution for handling face detection and recognition tasks without extensive model training.

**Features and Functionality**  
The core features of the application include:
- Uploading tagged photos to build a known faces database.
- Verifying uploaded photos to ensure they contain a detectable face.
- Real-time face recognition using a camera feed.
- Detection of unknown faces, labeled as "intruders."
- A user-friendly interface for managing the face database, including deleting specific tags and their associated photos.

**Structure and Files**  
The project consists of the following core components:
- **`app.py`**: The main Flask application script, responsible for routing and backend logic. It includes endpoints for uploading photos, starting the camera, and managing the face database.
- **`face_recognition_v3.py`**: A custom module for handling face recognition tasks. It contains functions for loading known faces, encoding them, and starting the camera feed for real-time recognition. Key functions include:
  - `load_known_faces`: Loads and encodes known face images from the specified directory.
  - `start_camera`: Activates the webcam, processes the video feed, and performs real-time face recognition, drawing bounding boxes and labels for detected faces.
- **`templates/`**: Contains HTML templates for rendering the web interface, including pages for uploading photos, managing faces, and starting recognition.
- **`static/`**: A directory for static files like CSS and JavaScript to enhance the application's frontend design.
- **`known_faces/`**: A directory to store uploaded photos of tagged individuals.
- **`README.md`**: Documentation for the project, detailing its purpose, structure, and design decisions.

**Design Decisions**  
1. **Modular Design**: The application is split into clearly defined modules to ensure scalability and ease of maintenance.
2. **Face Verification**: Uploaded photos are verified to contain a detectable face to maintain the integrity of the database.
3. **Real-Time Processing**: The camera feed is downscaled for processing to optimize performance without sacrificing recognition accuracy.
4. **User-Friendly UI**: The interface is designed to make it intuitive for users to upload photos, manage the database, and start recognition.

**Challenges and Learning**  
During the development of this project, several challenges were encountered:
- **Face Verification**: Ensuring uploaded photos had detectable faces required careful handling of edge cases.
- **Real-Time Recognition**: Optimizing the camera feed for smooth real-time performance was a technical hurdle.
- **File Management**: Handling multiple uploads and maintaining a clean directory structure for tagged photos was crucial.
- **Recognition Accuracy**: Ensuring accurate recognition required tuning parameters and testing with diverse datasets.
- **Exploring Alternatives**: The initial attempt to use YOLO highlighted the importance of selecting the right tools for the project's scope and requirements.

These challenges helped reinforce skills in Flask, face recognition libraries, and file handling in Python.

**Future Improvements**  
Given more time and resources, the following improvements could be made:
- Adding support for multiple camera feeds.
- Enhancing face recognition accuracy using advanced deep learning models.
- Providing analytics on face recognition activity, such as timestamps and frequency of intruder detections.
- Enabling cloud storage for known faces to make the database accessible across devices.
- Implementing mobile and IoT integrations to expand usability.

**Conclusion**  
This project demonstrates the application of face recognition technologies in a practical, real-world scenario. It highlights the potential for using machine learning and Python-based frameworks to build robust, user-centric applications. The app provides a strong foundation for further development and integration with advanced features like cloud-based storage and analytics.

---

Thank you for exploring this project. For any questions or feedback, feel free to reach out!

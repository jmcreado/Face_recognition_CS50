## Overview
This document outlines the technical and design decisions made during the development of the Face Recognition Application. It details the architecture, component interactions, and the reasoning behind major choices in implementation.

---

## Architecture

The application follows a modular architecture to separate concerns and ensure scalability. The major components are:

1. **Frontend (HTML Templates):** Provides a user-friendly interface for uploading photos, starting the camera, and managing the face database.
2. **Backend (Flask Application):** Handles HTTP requests, routes, and backend logic.
3. **Face Recognition Module (`face_recognition_v3.py`):** Contains functions for loading known faces, processing camera feeds, and performing recognition tasks.

### Flow
- Users upload images via the web interface.
- Images are stored in the `known_faces/` directory after verification.
- The `start_camera` function in `face_recognition_v3.py` uses OpenCV to capture a video feed and processes frames to detect and recognize faces in real time.

---

## Design Decisions

### Choice of Technology
1. **Flask Framework:** Selected for its lightweight and modular nature, making it ideal for small to medium-sized applications.
2. **`face_recognition` Library:** Provides pre-built face detection and recognition capabilities, reducing the need for extensive model training.
3. **YOLO vs. `face_recognition`:**
   - Initial experiments with YOLO were abandoned due to its computational requirements and inefficiency for the volume of data. `face_recognition` proved to be a simpler and more effective choice for the project’s scale and objectives.

### File Handling
- The `known_faces` directory serves as the repository for user-uploaded photos.
- Each file is checked for valid image format and the presence of a detectable face before being accepted.

### Performance Optimization
- Frames captured by the webcam are downscaled by a factor of 4 to improve processing speed without compromising accuracy.
- Only faces detected in a frame are processed further for recognition, reducing unnecessary computations.

---

## Key Functions

### `load_known_faces`
- Encodes faces from images in the `known_faces` folder.
- Uses filenames as tags for the recognized faces.
- Validates that each image contains exactly one detectable face.

### `start_camera`
- Captures video feed using OpenCV.
- Processes each frame to detect and recognize faces.
- Draws bounding boxes around recognized faces and labels them with tags or "INTRUDER."

---

## Challenges

1. **Real-Time Processing:**
   - Achieving smooth video feed and recognition required careful downscaling and optimization of frame processing.
2. **File Validation:**
   - Ensuring that only valid images with detectable faces are stored was critical to maintaining database integrity.
3. **Exploration of Alternatives:**
   - Time was spent exploring YOLO, which provided valuable insights into the strengths and weaknesses of different face detection methods.

---

## Future Considerations

- Implementing advanced models to improve recognition accuracy.
- Adding support for multiple video sources.
- Enhancing the frontend interface with real-time statistics and analytics.
- Storing face data and logs in a secure cloud environment for scalability and cross-device compatibility.

---

## Conclusion

This design approach ensures that the application is robust, efficient, and user-friendly. By focusing on modularity and leveraging efficient libraries, the project achieves its objective while providing a foundation for future enhancements.
